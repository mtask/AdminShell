from fabric.api import *
from fabric.tasks import execute
import sys, os


class remote(object):

    def get_hosts(self):
        self.hosts = []
        self.users = []
        with open('hosts.txt','r') as h:
            for self.l in h:
                self.params = self.l.split('=', 1)
                self.hosts.append(self.params[0])
                self.users.append(self.params[1])
        
        return (self.hosts, self.users)
        
            
    def run_cmd(self, cmd_raw):
        self.failed = []
        self.cmd = cmd_raw.split()
        self.servers,self.users = self.get_hosts()
        for self.s, self.u in zip(self.servers, self.users):
            if not os.path.isfile('~/.ssh/id_rsa'):
                with settings(host_string=self.s, user=self.u):
                    try:
                        if "sudo" in self.cmd:
                            self.cmd.remove('sudo')
                            sudo(' '.join(self.cmd))
                        else:
                            run(' '.join(self.cmd))
                       
                    except Exception as e:
                        self.failed.append(self.s)
                        print "Execution failed on: "+self.t
                        print "Error:"+str(e)
                        
            else:
                #Change path to match your private key
                with settings(host_string=self.s, user=self.u, key_filename='~/.ssh/id_rsa'):
                    try:
                        if "sudo" in self.cmd:
                            self.cmd.remove('sudo')
                            sudo(' '.join(self.cmd))
                        else:
                           run(' '.join(self.cmd))
                       
                    except Exception as e:
                        self.failed.append(self.t)
                        print "Execution failed on: "+self.s
                        print "Error:"+str(e)

        if len(self.failed) == 0:
            print "Operstion successfull on all hosts"
        else:
            print "[!] Execution failed on:"
            for f in self.failed:
                print f

                                     
if __name__=='__main__':
    pass