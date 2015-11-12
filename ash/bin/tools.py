#!/usr/bin/python
import os, time, subprocess, re, socket, getpass
from IPy import IP
import SimpleHTTPServer, SocketServer

class netmon(object):
    def log(self, state):
        self.int_down = ' --> Internet connection down.'
        self.dns_down = ' --> DNS failed - Internet connection up.'
        self.up_again = ' --> Connection up again.'
        self.s = state
        if self.s == "start":
            self.write_log(">Monitoring<")
        elif self.s == "stop":
            self.write_log(">end<")
        elif self.s == 'ping_down':
            self.write_log(self.int_down)
            
        elif self.s == 'ping_up_dns_down':
            self.write_log(self.dns_down)
            
        elif self.s == 'up_again':
            self.write_log(self.up_again)
                   
    def write_log(self, data):
        self.clock = str("\n"+time.strftime("%X"))
        self.data = self.clock+data
        self.date_raw = str(time.strftime("%x"))
        self.log_name = "conmon_"+re.sub('[/]', '_', self.date_raw)+'.log'
        if os.path.isfile(self.log_name):
            self.l = open(self.log_name, 'a')
        else:
            self.l = open(self.log_name, 'w')
        self.l.write(self.data)
        self.l.close()
    
            
    def ping(self, targ):
        self.t = targ
        if os.name == 'posix':
            self.output = subprocess.check_output("ping -w 1 -c 1 "+self.t+" | grep icmp* | wc -l" , shell=True)
            #output is 0 or 1
                  
        else:
            self.output_raw = subprocess.check_output("ping -n 1 " +self.t)
            if "Received = 1" in self.output_raw:
                self.output = "1"
            else:
                self.output = "0"
                       
        return self.output
            
    def monitor(self,time_, interval):
        try:
            self.time_ = time.time() + (60 * int(time_))
            self.i_val = int(interval)*60
            self.dns = False
            self.up = True
            self.log("start")
        
            while time.time() < self.time_:
                if not self.dns:
                    self.ping_ = self.ping('8.8.8.8')
                    if '0' in self.ping_:
                        if self.up:
                            self.log('ping_down')
                            self.up = False
                        
                    else:
                        if not self.up:
                            self.log('up_again')
                            self.up = True
 
            
                if self.dns:
                    self.ping_d = self.ping('google.com') #used if --dns selected
                    self.ping_ = self.ping('8.8.8.8')
                    if '0' in self.ping_d:
                        if '0' in self.ping_:
                            if self.up:
                                self.log('ping_down')
                                self.up = False
                            
                        elif '1' in self.ping_:
                            self.log('ping_up_dns_down')
                            self.up = False
                    else:
                        if not self.up:
                            self.log('up_again')
                            self.up = True        
                time.sleep(self.i_val)
            self.log("stop")
            return True
       
        except:
            return False



class ip_mac_harvest(object):
##ip_mac_harvest pulls IP and MAC addresses from given file     

    def harvest(self, file_):
    
        self.ips = []
        self.macs = []
        self.file_ = file_
        if not os.path.isfile(self.file_):
            print "No such file: "+self.file_
            return
    
        with open(self.file_, 'r') as f:
            for self.line in f:
                self.wrds = self.line.split(' ')
                for self.wrd in self.wrds:
                    self.ips_raw = re.findall( r'[0-9]+(?:\.[0-9]+){3}', self.wrd )
                    for self.ip in self.ips_raw:
                        if IP(self.ip): 
                             self.ips.append(self.ip)                 
     
                    self.macs_raw = re.findall("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", self.wrd.lower())
                    self.macs.extend(self.macs_raw)
                    
                            
        return (self.ips, self.macs)
        

class lookup(object):
    
    def get_host(self, target):
        self.t = target
        if re.findall( r'[0-9]+(?:\.[0-9]+){3}', self.t):
            try:
                self.res = socket.gethostbyaddr(self.t)
                return self.res[0]         
            except socket.gaierror:
                return "Couldn't find any results for: " +str(self.t)
            except Exception as e:
                print e
        else:
            try:
                self.res = socket.gethostbyname(self.t)
                return self.res
            except socket.gaierror:
                return "Couldn't find any results for: " +str(self.t)
            except Exception as e:
                print e
        
class file_sharing(object):
     
    def simple_share(self, path, port):
        self.curr_dir = os.getcwd()
        self.path = path
        os.chdir(self.path)
        self.port = int(port)
        self.handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        self.httpd = SocketServer.TCPServer(("", self.port), self.handler)
        print "Running at port: "+str(self.port)
        print "Sharing files under: "+self.path
        try:
           self.httpd.serve_forever()
        except KeyboardInterrupt:
           print "Sharing stopped"
           os.chdir(self.curr_dir)
           return
        except:
           print "[!] Print error while running server"
        finally:
            self.httpd.shutdown()     
    
if __name__ == '__main__':
    pass