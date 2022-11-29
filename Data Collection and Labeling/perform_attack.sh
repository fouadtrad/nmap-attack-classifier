#!/bin/sh

# Author: Fouad Trad

#Parameters provided when running the file: Attack type, IPvictim, number of repetitions

attack=$1 #The attack type
ip=$2 #The victim's IP
number=$3 #How many times we will perform the attack


ping="PINGONLY"
fin="TCPFIN"
syn="TCPSYN"
null="TCPNULL"
xmas="XMAS"
ack="TCPACK"
udp="UDP"
tcp="TCP"
tcpwindow="TCPWINDOW"
tcpmaimon="TCPMAIMON"
echoping="ECHOPING"
timeping="TIMEPING"
ipping="IPPING"
portscan="PORTSCAN"
osdetect="OSDETECT"
serviceversionscan="SERVICEVERSIONSCAN"


i=0 # a counter

while [ $i -le $number ]
do
	if [ $attack = $ping ]
		then
		echo "ping"
		sudo nmap -sP $ip --disable-arp-ping
	elif [ $attack = $fin ]
		then 
		echo "fin"
		sudo nmap -sF $ip
	elif [ $attack = $syn ]
		then 
		echo "syn"
		sudo nmap -sS $ip
	elif [ $attack = $null ]
		then
		echo "null"
		sudo nmap -sN $ip
	elif [ $attack = $xmas ]
		then
		echo "xmas"
		sudo nmap -sX $ip
	elif [ $attack = $ack ]
		then
		echo "ack"
		sudo nmap -sA $ip
	elif [ $attack = $udp ]
		then
		echo "udp"
		sudo nmap -sU $ip 
	elif [ $attack = $tcp ]
		then
		echo "tcp"
		sudo nmap -sT $ip
	elif [ $attack = $echoping ]
		then 
		echo "echo ping"
		sudo nmap -PE $ip
	elif [ $attack = $timeping ]
		then 
		echo "time ping"
		sudo nmap -PP $ip
	elif [ $attack = $ipping ]
		then 
		echo "ip ping"
		sudo nmap -PO $ip
	elif [ $attack = $portscan ]
		then 
		echo "fast port scan"
		sudo nmap -F $ip
	elif [ $attack = $osdetect ]
		then 
		echo "OS Detection"
		sudo nmap -O $ip
	elif [ $attack = $serviceversionscan ]
		then 
		echo "Service version detection"
		sudo nmap -sV $ip
	elif [ $attack = $tcpwindow ]
		then 
		echo "TCP window scan"
		sudo nmap -sW $ip
	elif [ $attack = $tcpmaimon ]
		then 
		echo "TCP maimon scan"
		sudo nmap -sM $ip
	fi
	i=$(( $i + 1 ))
	sleep 0.5
done
