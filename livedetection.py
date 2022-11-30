from pathlib import Path
import pandas as pd
import os 
import pyinotify
import warnings
from classifier.classifier import *

warnings.filterwarnings("ignore")
dir_path = Path(os.path.realpath(__file__)).parent

# read the csv file
try:
    df = pd.read_csv('./data_to_monitor/log.csv')
    old_len = len(df)
    new_len = len(df)
except:
    old_len = 0
    new_len = 0
    
# initialize the classifier
model_path = dir_path / "classifier/model.sav"
features_path = dir_path / "classifier/features.txt"
classifier = Classifier(model_path, features_path)

# set  the event triggered by the kdd_feature_extractor after the csv file is edited
columns = ['Duration',	'Protocol Type',	'Service',	'Flag',	'Src Bytes',	'Dst Bytes',	'Land',	'Wrong Fragment',	'Urgent',	'Count',	'Srv Count',	'Serror Rate',	'Srv Serror Rate',	'Rerror Rate',	'Srv Rerror Rate', 	'Same Srv Rate', 	'Diff Srv Rate',	'Srv Diff Host Rate', 	'Dst Host Count',	'Dst Host Srv Count',	'Dst Host Same Srv Rate',	'Dst Host Diff Srv Rate',	'Dst Host Same Src Port Rate',	'Dst Host Srv Diff Host Rate',	'Dst Host Serror Rate',	'Dst Host Srv Serror Rate',	'Dst Host Rerror Rate',	'Dst Host Srv Rerror Rate']
def on_change(ev):
    print("changed")
    
    # reads the file
    df = pd.read_csv('./data_to_monitor/log.csv')
    global old_len, new_len
    old_len = new_len
    new_len = len(df)

    # get the changed rows (added rows)
    updated_rows = new_len - old_len
    added_rows = df.tail(updated_rows)
    added_rows.columns = columns

    # transform the dataframe to list of dictionaries
    predictions=[]
    added_rows_dict = added_rows.to_dict('records')
    
    # predict using the models
    for row in added_rows_dict:
        #print(classifier.predict(row))
        predictions.append(classifier.predict(row))
    
    # display predictions
    pred_df = pd.DataFrame({'classes':predictions})
    print(pred_df['classes'].value_counts(normalize=True))

# attach event to the changes of the csv file
wm = pyinotify.WatchManager()
wm.add_watch('./data_to_monitor/log.csv', pyinotify.IN_MODIFY, on_change)
notifier = pyinotify.Notifier(wm)
notifier.loop()
