from pathlib import Path
import pandas as pd
import os 
import pyinotify
import warnings
from classifier import *

warnings.filterwarnings("ignore")
dir_path = Path(os.path.realpath(__file__)).parent
try:
    df = pd.read_csv('./data_to_monitor/log.csv')
    old_len = len(df)
    new_len = len(df)
except:
    old_len = 0
    new_len = 0
model_path = dir_path / "model.sav"
features_path = dir_path / "features.txt"
classifier = Classifier(model_path, features_path)

columns = ['Duration',	'Protocol Type',	'Service',	'Flag',	'Src Bytes',	'Dst Bytes',	'Land',	'Wrong Fragment',	'Urgent',	'Count',	'Srv Count',	'Serror Rate',	'Srv Serror Rate',	'Rerror Rate',	'Srv Rerror Rate', 	'Same Srv Rate', 	'Diff Srv Rate',	'Srv Diff Host Rate', 	'Dst Host Count',	'Dst Host Srv Count',	'Dst Host Same Srv Rate',	'Dst Host Diff Srv Rate',	'Dst Host Same Src Port Rate',	'Dst Host Srv Diff Host Rate',	'Dst Host Serror Rate',	'Dst Host Srv Serror Rate',	'Dst Host Rerror Rate',	'Dst Host Srv Rerror Rate']
def on_change(ev):
    print("changed")
    df = pd.read_csv('./data_to_monitor/log.csv')
    global old_len, new_len
    old_len = new_len
    new_len = len(df)

    updated_rows = new_len - old_len
    added_rows = df.tail(updated_rows)
    added_rows.columns = columns

    predictions=[]
    added_rows_dict = added_rows.to_dict('records')
    
    for row in added_rows_dict:
        #print(classifier.predict(row))
        predictions.append(classifier.predict(row))
    
    pred_df = pd.DataFrame({'classes':predictions})
    print(pred_df['classes'].value_counts(normalize=True))

wm = pyinotify.WatchManager()
wm.add_watch('./data_to_monitor/log.csv', pyinotify.IN_MODIFY, on_change)
notifier = pyinotify.Notifier(wm)
notifier.loop()
