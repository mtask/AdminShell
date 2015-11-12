AdminShell(ash) is shell-like enviroment with various tools for aspiring Linux sysadmins. Ash supports tab autocompletion and command history with up arrow(only current session at the moment).

###Depencies

$ pip install IPy fabric netifaces scapy

## Start ash session

&gt; python ash.py

##Available commands

###pydump

Packet analyzing tool made with scapy

arguments:

  -i IFACE, --iface IFACE    Capturing interface

optional arguments:
  
  -h, --help            show this help message and exit
    
  -n NUM, --num NUM     Number of packets to capture
  
  -r READ, --read READ  Read .pcap file
  
  -f FILTER, --filter FILTER      Filter packets. Use quotes("")

  -w WRITE, --write WRITE         Write capture to file
 
  -I, --inspect         Inspect packets
 
  -v, --verbose         verbose output

###multissh

Remotely run commands on multiple ssh servers.

Basic usage: &gt; multissh [command]

Run local script on host(s): &gt; multissh -script [script_name]

Run local script with sudo: &gt; multissh -script sudo [script_name]

Copy file from host(s): &gt;multissh -copy [remotepath] [localpath]

Copy file to host(s):&gt;multissh -put [localpath] [remotepath]

Modify multissh.conf file in ash's directory with the following form with one host+user per line:"[user@host]=[user]" (without quotes).
Multissh can ofcourse be used also to run remote commands in one server only. Hosts can be commented out with "#", so certain hosts can be skipped without removing them. When running local scripts the script is copied to host and then executed.

###keyparser

Usage: &gt; keyparser --path [authorized_keys_file_path]

Parse keys and options from authorized_keys file to SQLite database.

Default path to authorized_keys is set to "~/.ssh/". Custom path can be set with "--path [PATH]" argument.

Structure of auth_keys.db:

+----+---------------+--------------+

| id |      key      | option names |

+----+---------------+--------------+

|  1 | ssh-rsa AA... | options      |

+----+---------------+--------------+

###netmon

Usage: &gt; netmon [time]  [interval]

time - Monitoring time

interval - Connection status checking interval.

With netmon command you can start internet connection status monitoring in background. Monitoring lasts for given time and internet connection is checked for given interval. It logs connection's down times and if connection has been restored. Monitorin and interval time is given in minutes. Monitoring will be finished even if user exits from ash's shell.

###harvest

Usage: &gt; harvest  [file] -s

file - Path to file where to harvest addresses

-s  Save finds to file(optional)

With harvest command you can find IP and MAC addresses from given file. It prints findings to screen but you can also save results to file. Saved files are stored in ash's directory.

###lookup

Simple dns lookup.

Usage: &gt; lookup [address/domain]

###quick_share

Quickly share files under given path. WARNING: With quick_share no authentication is needed to access shared files.

Usage: &gt; quick_share [path] [port]

###ipconf

Usage: &gt; ipconf

Get list of network interfaces with ip addresses.

Prints Interface+ip-address+mac-address.

###sweep

Usage: &gt; sweep

Fast network ping sweep 


###Other commands

help - Print help page. Add command name after help to get more info

clear - Clear screen

ls - List files

pwd - Get cwd path

exit - Exit
