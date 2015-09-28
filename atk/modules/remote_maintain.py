from fabric.api import *
from fabric.tasks import execute
import sys, os


class remote(object):

    def get_hosts(self):
        self.hosts = []
        self.users = []
        try:
            with open('hosts.txt','r') as h:
                for self.l in h:
                    if self.l.startswith("#"):
                        continue
                    self.params = self.l.split('=', 1)
                    self.hosts.append(self.params[0])
                    self.users.append(self.params[1])
            return (self.hosts, self.users)
        except:
            "[!] Check your hosts.txt file for misconfiguration"

    def run_script(self,scmd,sudo_=False):
        put(scmd, scmd, mode=0755)
        if sudo_:
            sudo("./"+scmd)
        else:
            run("./"+scmd)
                  
    def run_cmd(self, cmd_raw):
        self.failed = []
        self.cmd = cmd_raw.split()
        self.servers,self.users = self.get_hosts()
        for self.s, self.u in zip(self.servers, self.users):
            if not os.path.isfile('~/.ssh/id_rsa'):
                with settings(host_string=self.s, user=self.u, warn_only=True):
                    try:
                        if "sudo" in self.cmd:
                            self.cmd.remove('sudo')
                            if "-script" in self.cmd:
                                self.cmd.remove("-script")
                                self.cmd = ''.join(self.cmd)
                                self.run_script(self.cmd, sudo_=True)                                
                            else:
                                sudo(' '.join(self.cmd))
                        else:
                            if "-script" in self.cmd:
                                self.cmd.remove("-script")
                                self.cmd = ''.join(self.cmd)
                                self.run_script(self.cmd)
                                
                            elif "-copy" in self.cmd:
                                self.cmd.remove("-copy")
                                self.r_path = self.cmd[0]
                                self.l_path = self.cmd[1]
                                get(self.r_path, self.l_path)
                           
                            elif "-put" in self.cmd:
                                self.cmd.remove("-put")
                                self.l_path = self.cmd[0]
                                self.r_path = self.cmd[1]
                                put(self.l_path, self.r_path)

                            else:
                                run(' '.join(self.cmd))
                       
                    except Exception as e:
                        self.failed.append(self.s)
                        print "Execution failed on: "+self.s
                        print "Error:"+str(e)

                        
            else:
                #Fix this, can't assume path to private_key
                with settings(host_string=self.s, user=self.u, key_filename='~/.ssh/id_rsa', warn_only=True):
                    try:
                        if "sudo" in self.cmd:
                            self.cmd.remove('sudo')
                            sudo(' '.join(self.cmd))
                        else:
                           run(' '.join(self.cmd))
                       
                    except Exception as e:
                        self.failed.append(self.s)
                        print "Execution failed on: "+self.s
                        print "Error:"+str(e)

        if len(self.failed) > 0:
            print "[!] Execution failed on:"
            for f in self.failed:
                print f

                                     
if __name__=='__main__':
    pass