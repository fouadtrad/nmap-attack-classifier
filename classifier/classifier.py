# Author: Saiid El Hajj Chehade

import pickle
from pathlib import Path
import pandas as pd
import os
import torch as ch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

dir_path = Path(os.path.realpath(__file__)).parent

class FeaturesSubset:
  def __init__(self, features, to_numpy=True):
        self.features = features
        self.to_numpy = to_numpy

  def transform(self, X, **transform_params):
        if self.to_numpy:
          return pd.DataFrame(X[self.features]).values
        else:
          return pd.DataFrame(X[self.features])

  def fit_transform(self, X, y, **transform_params):
        return self.transform(X, **transform_params)

  def fit(self, X, y=None, **fit_params):
    return self


class Classifier:

    def __init__(self, model_pickle_path: Path, features_fp: Path):
        """Load model and features from pickle files

        Args:
            model_pickle_path (Path): Path to model pickle file
            features_fp (Path): Path to features pickle file

        """
        self.model = pickle.load(open(str(model_pickle_path.resolve()), 'rb'))

        with open(str(features_fp.resolve()), 'r') as f:
            self.features = f.read().splitlines()

    def predict(self, x: dict) -> str:
        """Predict class for given features

        Args:
            x (dict): Features that must have keys from features.txt or classifier.features

        Returns:
            str: Predicted class
        """
        
        assert all([feature in x.keys() for feature in self.features]), "Missing features"
        
        x = {k: v for k, v in x.items() if k in self.features}
        
        x_df = pd.DataFrame([x, ])
        return self.model.predict(x_df)[0]
      
     
    
    
    
"""
NN Model Architecture (required for loading model)
    - 5 fully connected layers with tunable sizes (set to 128 -> 256 -> 512 -> 256 -> 128 in experiments)
    - ReLU activation after each FC layer (except for the last)
    - Optional batch normalization layers (with learnable parameters) applied after each FC layer (except for the last)
    - Optional dropout applied to each FC layer (except for the last)
"""
class FCN(nn.Module):
    def __init__(self, n_features, n_classes, n_nodes, batch_norm = False, dropout = False):
        super().__init__()
        self.input = nn.Linear(n_features, n_nodes['fc1'])
        self.fc1 = nn.Linear(n_nodes['fc1'], n_nodes['fc2'])
        self.fc2 = nn.Linear(n_nodes['fc2'], n_nodes['fc3'])
        self.fc3 = nn.Linear(n_nodes['fc3'], n_nodes['fc4'])
        self.fc4 = nn.Linear(n_nodes['fc4'], n_nodes['fc5'])
        self.fc5 = nn.Linear(n_nodes['fc5'], n_classes)

        self.batch_norm = batch_norm
        self.bn1 = nn.BatchNorm1d(n_nodes['fc2'])
        self.bn2 = nn.BatchNorm1d(n_nodes['fc3'])
        self.bn3 = nn.BatchNorm1d(n_nodes['fc4'])
        self.bn4 = nn.BatchNorm1d(n_nodes['fc5'])

        self.dropout = dropout
        self.drop = nn.Dropout(0.1)


    def forward(self, x):
        if self.dropout:
            if self.batch_norm:
                x = self.input(x)
                x = F.relu(self.drop(self.bn1(self.fc1(x))))
                x = F.relu(self.drop(self.bn2(self.fc2(x))))
                x = F.relu(self.drop(self.bn3(self.fc3(x))))
                x = F.relu(self.drop(self.bn4(self.fc4(x))))
                x = self.fc5(x)

            else:
                x = self.input(x)
                x = F.relu(self.drop(self.fc1(x)))
                x = F.relu(self.drop(self.fc2(x)))
                x = F.relu(self.drop(self.fc3(x)))
                x = F.relu(self.drop(self.fc4(x)))
                x = self.fc5(x)
        
        else:
            if self.batch_norm:
                x = self.input(x)
                x = F.relu(self.bn1(self.fc1(x)))
                x = F.relu(self.bn2(self.fc2(x)))
                x = F.relu(self.bn3(self.fc3(x)))
                x = F.relu(self.bn4(self.fc4(x)))
                x = self.fc5(x)

            else:
                x = self.input(x)
                x = F.relu(self.fc1(x))
                x = F.relu(self.fc2(x))
                x = F.relu(self.fc3(x))
                x = F.relu(self.fc4(x))
                x = self.fc5(x)

        return x    
      
class NN_Classifier:
    def __init__(self, model_path: Path, features_fp: Path, encoding_path: Path, means_path: Path, vars_path: Path):
        """Load model from a .pt file and features & encoding dictionaries from pickle files
        Args:
            model_pickle_path (Path): Path to model .pt file
            features_fp (Path): Path to features pickle file
            encoding_path (Path): Path to encoding dictionaries pickle file
        """
        self.model = ch.load(str(model_path.resolve())).to('cpu')
        self.means = np.load(str(means_path.resolve()))
        self.stdevs = np.sqrt(np.load(str(vars_path.resolve())))
        self.encoding_maps = pkl.load(open(str(encoding_path.resolve()), "rb"))

        with open(str(features_fp.resolve()), 'r') as f:
            self.features = f.read().splitlines()

    def predict(self, x: dict) -> str:
        """Predict class for given features
        Args:
            x (dict): Features that must have keys from features.txt or classifier.features
        Returns:
            str: Predicted class
        """
        
        assert all([feature in x.keys() for feature in self.features]), "Missing features"
        
        x = {k: v for k, v in x.items() if k in self.features}
        
        x_df = pd.DataFrame([x, ])

        # Categorical Encoding
        x_df['Protocol Type'] = self.encoding_maps[0][x_df['Protocol Type'].item()]
        x_df['Service'] = self.encoding_maps[1][x_df['Service'].item()]
        x_df['Flag'] = self.encoding_maps[2][x_df['Flag'].item()]

        # Scaling
        num_features = x_df.drop(['Protocol Type', 'Service', 'Flag'], axis = 1).columns.to_numpy()
        x_df[num_features] = (x_df[num_features] - self.means) / self.stdevs

        # Inference
        x = ch.from_numpy(x_df.to_numpy(copy = True)).type(ch.float)
        self.model.eval()
        y = self.model(ch.cat((x, x))).argmax(1)[0]

        return self.encoding_maps[3][y.item()]

      
      
# an example of how to use the classifier
if __name__ == "__main__":
    
    # you set the files paths
    model_path = dir_path / "model.sav"
    nn_classifier_path = dir_path / "nn_classifier.pt"
    features_path = dir_path / "features.txt"
    encoding_path = dir_path / "encoding_maps.p"
    means_path = dir_path / "means.npy"
    vars_path = dir_path / "vars.npy"
    
    classifier = Classifier(model_path, features_path)
    nn_classifier = NN_Classifier(nn_classifier_path, features_path, encoding_path, means_path, vars_path)
    
    test_input = {
    "Duration": 0,	
    "Protocol Type":"tcp",	
    "Service":"other",	
    "Flag":"OTH",	
    "Src Bytes":60,	
    "Dst Bytes":0,	
    "Land":0,	
    "Wrong Fragment":0,	
    "Urgent":0,	
    "Count":109,	
    "Srv Count":86,	
    "Serror Rate":0,	
    "Srv Serror Rate":0,	
    "Rerror Rate":0,	
    "Srv Rerror Rate":0,	
    "Same Srv Rate":0.79,	
    "Diff Srv Rate":0.21,	
    "Srv Diff Host Rate":0,	
    "Dst Host Count":50,	
    "Dst Host Srv Count":44,	
    "Dst Host Same Srv Rate":0.88,	
    "Dst Host Diff Srv Rate":0.12,	
    "Dst Host Same Src Port Rate":0.98,
    "Dst Host Srv Diff Host Rate":0,	
    "Dst Host Serror Rate":0,	
    "Dst Host Srv Serror Rate":0,	
    "Dst Host Rerror Rate":0,	
    "Dst Host Srv Rerror Rate":0,
    }
    
    print("Test Prediction:", classifier.predict(test_input))
    print("NN Classifier Test Prediction:", nn_classifier.predict(test_input))
