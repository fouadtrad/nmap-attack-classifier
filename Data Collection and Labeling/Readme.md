# Documentation
The scripts in this folder are to collect data and label it.
To run these scripts, we need 2 machines: an attacker's machine (A) and a victim's machine (B)

## Machine A:
On machine A, we just have to perform the nmap attacks. To do so, we run the shell script "perfromAttack.sh" and we specify as parameters the attack name, the destination IP and the number of times we want to perform the attack.
A full list on the name of attacks that can be handled exist inside the file.

Example Usage to perform a TCP SYN scan 2 times on a machine with IP 192.168.1.5:

```
sh performAttack.sh "TCPSYN" 192.168.1.5 2
```

## Machine B:

### Feature Extraction
On machine B, we capture the traffic while the attacks are being performed. For each attack we open a new wireshark session, and when the attack is done we save the resulting pcap files with the name of the attack (e.g. ack.pcap, syn.pcap, etc.).
To extract features from one pcap file, we use the kdd99_feature_extractor library [1]. The library gets a pcap file and returns the corresponding feature vectors. To save these feature vectors into a csv file, we can use the file **get_features.sh** which redirects the output of the library to a csv file.
Just for reference, we can run this script to extract features from live traffic or from pcap file, but in our study we used the option of pcap only, although both are coded.
To make things easier, once we have the pcap files, we run the script **get_csv_for_all_attacks.sh** which internally would call the script **get_features.sh** for each attack we have.
Just make sure the pcap files are within your current directory.
Example call:

```
sh get_csv_for_all_attcks.sh
```

### Data Labeling
After the previous step, we would have separate csv files for each possible attack. Here we run the python script **data_labeling.py** that aggregates all csv files into one data frame and assigns the corresponding label according to the name of the csv file.
After that, we can save our dataframe.

### Author:
Fouad Trad

## References:
[1] https://github.com/AI-IDS/kdd99_feature_extractor
