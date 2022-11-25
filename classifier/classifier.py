# Author: Saiid El Hajj Chehade

import pickle
from pathlib import Path
import pandas as pd
import os 
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


# an example of how to use the classifier
if __name__ == "__main__":
    
    # you set the files paths
    model_path = dir_path / "model.sav"
    features_path = dir_path / "features.txt"
    
    classifier = Classifier(model_path, features_path)
    
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
    
    print("Test prediction ", classifier.predict(test_input))