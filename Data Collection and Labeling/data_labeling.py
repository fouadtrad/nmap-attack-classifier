import pandas as pd
columns = ['Duration',	'Protocol Type',	'Service',	'Flag',	'Src Bytes',	'Dst Bytes',	'Land',	'Wrong Fragment',	'Urgent',	'Count',	'Srv Count',	'Serror Rate',	'Srv Serror Rate',	'Rerror Rate',	'Srv Rerror Rate', 	'Same Srv Rate', 	'Diff Srv Rate',	'Srv Diff Host Rate', 	'Dst Host Count',	'Dst Host Srv Count',	'Dst Host Same Srv Rate',	'Dst Host Diff Srv Rate',	'Dst Host Same Src Port Rate',	'Dst Host Srv Diff Host Rate',	'Dst Host Serror Rate',	'Dst Host Srv Serror Rate',	'Dst Host Rerror Rate',	'Dst Host Srv Rerror Rate', 'Src IP', 'Src Port','Dst IP' , 'Dst Port', 'Time']

def read_attack(path, name):
  #Function to get a path for a file, read it into a dataframe and then assign a label for it
  attack = pd.read_csv(path)
  attack.columns = columns
  attack['Class'] = name
  return attack

ack = read_attack("ack.csv", "ACK")
ackping = read_attack("ackping.csv", "ACKPING")
echoping = read_attack("echoping.csv", "ECHOPING")
fin = read_attack("fin.csv", "FIN")
ipping = read_attack("ipping.csv", "IPPING")
maimon = read_attack("maimon.csv", "MAIMON")
nul = read_attack("null.csv", "NUL")
osdetect = read_attack("osdetect.csv", "OSDETECT")
ping = read_attack("pingonly.csv", "PINGONLY")
portscan = read_attack("portscan.csv", "PORTSCAN")
window = read_attack("window.csv", "WINDOW")
servscan = read_attack("serviceversionscan.csv", "SERVICEVERSIONSCAN")
syn = read_attack("syn.csv", "SYN")
synping = read_attack("synping.csv", "SYNPING")
xmas = read_attack("xmas.csv", "XMAS")
udp = read_attack("udp.csv", "UDP")
udpping = read_attack("udpping.csv", "UDPPING")
timeping = read_attack("timeping.csv", "TIMEPING")
tcp = read_attack("tcp.csv", "TCP")
normal =  read_attack("normal.csv", "NORMAL")

#Concatenate the multiple classes into 1 dataframe
df = pd.concat([ack, ackping, echoping, fin, ipping, nul, osdetect, ping, portscan, window, maimon, servscan, syn, synping, xmas, udp, udpping, timeping, tcp, normal], axis=0, ignore_index=True)

# Save the result as a csv file
df.to_csv("Final_data.csv", index=False)

