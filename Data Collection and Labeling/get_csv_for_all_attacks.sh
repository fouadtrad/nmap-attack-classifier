#!/bin/sh

sh get_features ack.pcap ack.csv
sh get_features echoping.pcap echoping.csv
sh get_features portscan.pcap portscan.csv
sh get_features tcp.pcap tcp.csv
sh get_features ackping.pcap ackping.csv
sh get_features fin.pcap fin.csv
sh get_features timeping.pcap timeping.csv
sh get_features ipping.pcap ipping.csv
sh get_features udp.pcap udp.csv
sh get_features serviceversionscan.pcap serviceversionscan.csv
sh get_features udpping.pcap udpping.csv
sh get_features null.pcap null.csv
sh get_features osdetect.pcap osdetect.csv
sh get_features syn.pcap syn.csv
sh get_features xmas.pcap xmas.csv
sh get_features pingonly.pcap pingonly.csv
sh get_features synping.pcap synping.csv
sh get_features maimon.pcap maimon.csv
sh get_features window.pcap window.csv
sh get_features normal.pcap normal.csv

