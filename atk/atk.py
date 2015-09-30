#!/usr/bin/python
import os, threading, sys, cmd, getpass
from modules.tools import *
from modules.remote_maintain import *

"""
Copyright mtask@github.com
See LICENSE.md
"""

class atk(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "atk> "
                        
    def do_netmon(self, time_ival):
        """
        netmon [monitoring_time(minutes)] [interval(minutes)]
        Example: netmon 180 2
        Monitor internet connection status in background.
        Results are logged.
        """
        self.args = time_ival.split()
        self.nm = netmon()
        self.time = self.args[0]
        self.ival = self.args[1]
        self.monitord = threading.Thread(target=self.nm.monitor, args=(self.time,self.ival))
        self.monitord.daemon = True
        if self.monitord.start():
            print "[!] Monitoring internet connection in Background"
        else:
            print "[!] Monitoring Failed to start!"
    
    def do_harvest(self, args):
        """
        harvest [input_file] -s
        Harvest IP and MAC addresses from file.
        Parameter -s is optional for saving output to file.
        """
        self.imh = ip_mac_harvest()
        self.args = args.split()
        if len(self.args) < 1 or len(self.args) > 3:
            print "*** Check arguments"
            return
        if "-s" in self.args:
            if "-s" == self.args[0]:
                self.file_ = self.args[1]
        else:
            self.file_ = self.args[0]
        self.ips, self.macs = self.imh.harvest(self.file_)     
        print "IPs found("+str(len(self.ips))+"):"
        for ip in self.ips:
            print ip
        print "MAC-addresses found("+str(len(self.macs))+"):"
        for mac in self.macs:
            print mac
        #Write results to file if -s selected
        if "-s" in self.args:
            self.f_name = "harvested_"+self.file_+".txt"
            self.h = open(self.f_name, 'w')
            self.h.write("IPs found("+str(len(self.ips))+"):\n")
            for ip in self.ips:
                self.h.write(ip+"\n")
            self.h.write("\nMAC-addresses found("+str(len(self.macs))+"):")
            for mac in self.macs:
                self.h.write(mac)
              
    def do_lookup(self, target):
        """
        lookup [host]
        Dns lookup
        """
        self.t = target.split()
        if len(self.t) == 1:   
            self.lu = lookup()
        else:
            print "*** Check arguments"
        self.res = self.lu.get_host(target)
        print self.res
        
    def do_multissh(self, _cmd_):
        '''
        multissh [command]
        Run local script on remote machine:
        multissh -script [script_name]
        Run script with sudo:
        multissh -script sudo [script_name]
        Copy file from server(s):
        multissh -copy [remotepath] [localpath]
        Copy file to server(s):
        multissh -put [localpath] [remotepath]
        '''
        self.r = remote()
        self.r.run_cmd(_cmd_)
                                     
    def do_quick_share(self, path_port):
        """
        quick_share [path] [port]
        Quick file share under given path.
        WARNING: No authentication required to access files.
        """  
        self.args = path_port.split()
        if len(self.args) == 2:
            self.port = self.args[1]
            self.path =  self.args[0]
            self.fs = file_sharing()
            print "WARNING: With quick_share no authentication required to access files!"
            self.fs.simple_share(self.path, self.port)
        else:
            print "*** Check arguments"
        
    def do_clear(self,*args):
        """
        clear
        Clear screen.
        """
        os.system('clear')
        
    def do_ls(self,*args):
        '''
        ls
        List files and directories.
        '''
        len(''.join(args))
        if len(''.join(args)) == 0:
            self.pwd = '.'
        else:
            self.pwd = ''.join(args)       
        try:   
            self.files = os.listdir(self.pwd)
            for f in self.files:
               print f,
            print
        except Exception as e:
            print e

    def do_cd(self,path):
        '''Change working directory'''
        try:
            os.chdir(path)
        except:
            if path == "":
                self.home_dir = os.path.expanduser("~/")
                os.chdir(self.home_dir)
            else:
                print "*** No such file or directory: "+path           

    def do_pwd(self, *args):
       '''Shpw current working directory'''
       print os.getcwd()
        
    def do_exit(self,*args):
        '''exit'''
        sys.exit(0)
        
    def do_EOF(self,*args):
        print
        sys.exit()
    
    def cmdloop(self):
        try:
            cmd.Cmd.cmdloop(self)
        except KeyboardInterrupt:
            print 
            self.cmdloop()
        except TypeError as e:
            print "*** Invalid syntax"
            self.cmdloop()
        except IndexError as e:
            print "*** Check arguments"
            self.cmdloop()
            
if __name__=="__main__":
    atk().cmdloop()
    
