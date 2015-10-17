import netifaces, os

class ipconf(object):

    """
    Prints network interfaces info in simple and clean form
    Printed info includes Interface, ip-address and mac-address
    """

    def get_ifaces(self):
        self.iface_list = netifaces.interfaces()
        return self.iface_list
        
    def get_ifaceinfo(self, iface_=None):
        self.info_list = []
        if not iface_:
            self.ifaces = self.get_ifaces()
            print "Interface\tIP-address\tMAC-address"
            print "------------------------------------------"
            for self.iface in self.ifaces:
                try:
                    self.addrs = netifaces.ifaddresses(self.iface)
                    self.ip = self.addrs[netifaces.AF_INET][0]['addr']
                    print self.iface+"\t\t"+self.ip
                except Exception as e:
                   if e == "2":
                       continue
                   else:
                       #raise e
                       continue
                
                
    def get_mac(self):
       pass
       
                
if __name__ == '__main__':
    os.system('clear')
    ipconf().get_ifacinfo()  
            
        
