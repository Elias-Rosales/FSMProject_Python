#SYNTAX VERIFICATION CLASS
import sys
import re
class SV(object):
    #Properties
    FSM = "FSM.txt"
    FSM_txt = "FSM.txt"
    FSM_path = "FSM.txt"
    conf = "conf.ini"
    TestB = "testbench.sv"
    design = None
    design_path = None
    m = None
    #Constructor
    def __init__(self):
        self.Args()
        self.extensions()
        self.open_error()
        self.pathVerification()
        self.getFSM()
        self.getFSMpath()
    #Member Functions
    def Args(self):
        if (len(sys.argv) < 2):
            sys.stderr.write("\n[ERROR] No argument has been declared\n")
            print("\tUse the following syntax: main.py [FSM_file.txt] [Testbench_Name.sv] [conf.ini] [Design_Name.sv]")
            sys.exit(1)
        else:
            self.FSM_path = sys.argv[1]
            if (len(sys.argv) == 3):
                self.TestB = sys.argv[2]
            elif (len(sys.argv) == 4):
                self.TestB = sys.argv[2]
                self.conf = sys.argv[3]
            elif (len(sys.argv) == 5):
                self.TestB = sys.argv[2]
                self.conf = sys.argv[3]
                self.design_path = sys.argv[4]
        
    def extensions(self):
        if(not re.match(re.compile(r'^.*(.txt)$'),self.FSM_path)):
            sys.stderr.write(f"\n[ERROR] InputFileName = '{self.FSM_path}'\n")
            print("\tThe input file must have a .txt extension\n")
            sys.exit(1)
        if(not re.match(re.compile(r'^.*(.sv)$'),self.TestB)):
            sys.stderr.write(f"\n[ERROR] TestbenchFileName = '{self.TestB}'\n")
            print("\tThe testbench file must have a .sv extension\n")
            sys.exit(1)
        if (self.design_path!= None):
            if(not re.match(re.compile(r'^.*(.sv)$'),self.design_path)):
                sys.stderr.write(f"\n[ERROR] DesignFileName = '{self.design_path}'\n")
                print("\tThe design file must have a .sv extension\n")
                sys.exit(1)
        if(not re.match(re.compile(r'^.*(.ini)$'),self.conf)):
            sys.stderr.write(f"\n[ERROR] ConfFileName = '{self.conf}'\n")
            print("\tThe configuration file must have a .ini extension\n")
            sys.exit(1)

    def open_error(self):
        try:
            temps = self.FSM_path
            open(temps,'r')
            temps = self.conf
            open(temps,'r')
        except Exception:
            print (f"[ERROR] FileNotFound = No such file or directory: '{temps}'")
            sys.exit(1)

    def pathVerification(self):
        if(re.match(re.compile(r'^[a-zA-Z.].*[\\\/](\w+.txt)$'),self.FSM_path)):
            self.m = re.search(re.compile(r'^[a-zA-Z.].*[\\\/](\w+.txt)$'),self.FSM_path)
            self.FSM = self.m.group(1)
            self.FSM_txt = self.m.group(1)
        else:
            self.FSM = self.FSM_path
            self.FSM_txt = self.FSM_path
        if (self.design_path!= None):
            if(re.match(re.compile(r'^[a-zA-Z.].*[\\\/](\w+.sv)$'),self.design_path)):
                self.m = re.search(re.compile(r'^[a-zA-Z.].*[\\\/](\w+.sv)$'),self.design_path)
                self.design = self.m.group(1)
            else:
                self.design = self.design_path

    def getFSM(self):
        self.FSM = self.FSM.replace('.txt','.sv')
        #return self.FSM
    def getFSMpath(self):
        self.FSM_path = self.FSM_path.replace('.txt','.sv')
        #return self.FSM_path
    """def getTB(self):
        return self.TestB
    def getDesign(self):
        return self.design
    def getDesignpath(self):
        return self.design_path
    def getconf(self):
        return self.conf"""
    