#!/usr/bin/python

import os, sys

class protocols(object):

    def read_protocols(self):
        self.protocol_dict = {}
        
        if os.path.isfile('/etc/protocols'):
            with open('/etc/protocols') as protos:
                for self.line in protos:
                    if self.line.startswith("#"):
                        continue
                        
                    self.p = self.line.split()
                    if len(self.p) >= 3:
                        #print self.p
                        self.protocol_dict[self.p[1]] = self.p[2]
            print self.protocol_dict
                    