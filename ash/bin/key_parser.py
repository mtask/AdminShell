#!/usr/bin/python

'''
Author: mtask@github.com
Description: Key_parser parses keys and options from authorized_keys file to SQLite database.
It assumes that file can be found under path "~/.ssh/". Custom path can be set with "--path [PATH]" argument.

'''

import sqlite3, re, sys, os, argparse

class db_handler(object):

    ###############################################################
    #Function: create_db                                          #
    #Creates sqlite database for keys+options in authorized_keys  #
    #Database name: auth_keys.db.                                 #
    #table's schema:id,key,option names                           #
    ###############################################################
    def create_db(self):

        try:
            self.con = sqlite3.connect('auth_keys.db')
            self.c = self.con.cursor()
            self.c.execute('''CREATE TABLE  IF NOT EXISTS keys
                (id INTEGER PRIMARY KEY,
                key TEXT NOT NULL,
                "cert-authority" TEXT,
                command  TEXT,
                environment TEXT,
                "from" TEXT,
                "no-agent-forwarding" TEXT,
                "no-port-forwarding" TEXT,
                "no-pty" TEXT,
                "no-user-rc" TEXT,
                "no-X11-forwarding" TEXT,
                permitopen TEXT,
                principals TEXT,
                tunnel TEXT);''')

            self.con.commit()
        except Exception as e:
            self.con.rollback()
            raise e
        finally:
            self.con.close()


    ##################################################################
    #Function: insert_keys                                           #
    #Inserts keys+options to database auth_keys.db                   #
    #Options in form option="value" has null value in db if not used.#
    #Options that doesn't take value in form option="value" has value#
    #"enabled" or "disabled" in database.                            #
    ##################################################################
    def insert_keys(self, keys):

        self.keys = keys
        try:
            self.con = sqlite3.connect('auth_keys.db')
            self.c = self.con.cursor()

            self.c.executemany('''INSERT INTO keys
                (key,
                "cert-authority",
                command,
                environment,
                "from",
                "no-agent-forwarding",
                "no-port-forwarding",
                "no-pty",
                "no-user-rc",
                "no-X11-forwarding",
                permitopen,
                principals,
                tunnel) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''', self.keys)

            self.con.commit()
            print str(len(self.keys))+" keys added to auth_keys.db"
        except Exception as e:
            self.con.rollback()
            raise e
        finally:
            self.con.close()



class key_parser(object):

    ####################################################
    #Function:parse                                    #
    #Parses keys and options from authorized_keys file.#
    #Keys+options are returned in list of tuples.      #
    ####################################################
    def parse(self, path=os.path.expanduser("~/.ssh/")):

        self.authorized_keys = []
        self.ak_file = path+"authorized_keys"

        if not os.path.isfile(self.ak_file):
            print "[!] Error: authorized_keys file not found in "+path+"\n exiting..."
            sys.exit(0)

        with open(self.ak_file) as f:
            for line in f:
                self.key = []

                if "ssh-" in line:
                    if not line.startswith('ssh-'):
                        self.key_part = "ssh-"+line.split('ssh-')[1]
                        self.key.append(self.key_part)
                    else:
                        self.key.append(line)

                if "cert-authority" in line:
                    self.key.append("enabled")
                else:
                    self.key.append("disabled")
                if "command=" in line:
                    self.key.append(self.option_format("command", line))
                else:
                    self.key.append(None) #Appends none to match db table schema when inserting values to it.
                if "environment" in line:
                    self.key.append(self.option_format("environment", line))
                else:
                    self.key.append(None)
                if "from" in line:
                    self.key.append(self.option_format("from", line))
                else:
                    self.key.append(None)
                if "no-agent-forwarding" in line:
                    self.key.append("enabled")
                else:
                    self.key.append("disabled")
                if "no-port-forwarding" in line:
                    self.key.append("enabled")
                else:
                    self.key.append("disabled")
                if "no-pty" in line:
                    self.key.append("enabled")
                else:
                    self.key.append("disabled")
                if "no-user-rc" in line:
                    self.key.append("enabled")
                else:
                    self.key.append("disabled")
                if "no-X11-forwarding" in line:
                    self.key.append("enabled")
                else:
                    self.key.append("disabled")
                if "permitopen" in line:
                    self.key.append(self.option_format("permitopen", line))
                else:
                    self.key.append(None)
                if "principals" in line:
                    self.key.append(self.option_format("principals", line))
                else:
                    self.key.append(None)
                if "tunnel" in line:
                    self.key.append(self.option_format("tunnel", line))
                else:
                    self.key.append(None)

                if len(self.key) == 13:
                    self.authorized_keys.append(tuple(self.key))

        return self.authorized_keys


    ################################
    #Function: option_format       #
    #Returns option's value        #
    #e.g. option="this_is_returned"#
    ################################
    def option_format(self, option, options):
        self.op = option
        self.ops = options
        self.find_value = re.search(self.op+'="(.+?)"', self.ops)
        self.value = self.find_value.group(1)
        return self.value

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="authorized_keys file parser")
    parser.add_argument("-p", "--path",type=str, default="~/.ssh/", help="path to file, default ~/.ssh/")
    args = parser.parse_args()
    path = args.path

    db_handler().create_db()
    parsed_keys = key_parser().parse(path)
    db_handler().insert_keys(parsed_keys)
