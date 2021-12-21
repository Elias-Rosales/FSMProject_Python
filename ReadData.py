#READ DATA CLASS
from SyntaxVerification import SV
import re
import math

class ReadData(SV):
    #Attributes
    __pttrn_states = r"states\s*=\s*(.*);"
    __pttrn_initial_state = r"initial_state\s*=\s*(\w+);"
    __pttrn_inputs = r"inputs\s*=\s*(.*);"
    __pttrn_outputs = r"outputs\s*=\s*(.*);"
    __pttrn_in = r"in\s*=\s*(.*);"
    __pttrn_fsm = r"(\w+)\|\s*(.*)\|\s*(.*);"
    __pattern_timescale = r"^\s*timescale\s*=\s*(\w+\/\w+).*$"
    __pattern_delay = r"^\s*delay\s*=\s*(\#\d+).*$"
    __pattern_dumpvars = r"^\s*dumpvars\s*=\s*(\d+).*$"
    __pattern_cases = r"^\s*num_cases\s*=\s*(\d+).*$"
    __pattern_periodclk = r"^\s*period_clk\s*=\s*(\#\d+).*$"
    __pattern_version = r"^\s*version\s*=\s*(\d+).*$"
    __pattern_clk = r"^\s*clk\s*=\s*(\w+).*$"
    __pattern_rst = r"^\s*rst\s*=\s*(\w+).*$"
    __pattern_c_state = r"^\s*c_state\s*=\s*(\w+).*$"
    __pattern_n_state = r"^\s*n_state\s*=\s*(\w+).*$"
    __pattern_edge = r"^\s*edge\s*=\s*(\w+).*$"
    __pattern_active_rst = r"^\s*active_rst\s*=\s*(\d+).*$"
    timescale = None
    delay = None
    dumpvars = None
    num_cases = 0
    period_clk = None
    vers = 0
    clk = None
    rst = None
    c_state = None
    n_state = None
    edge = None
    active_rst=True
    conf_file = None
    book = None
    states_string = ""
    states = []
    initial_state = ""
    inputs = []
    inputs_s = []
    inputs_string = ""
    outputs = []
    outputs_s = []
    outputs_string = ""
    input_values = []
    next_state = {}
    output_state = {}
    num_bits_states = 0
    num_bits_inputs = 0
    num_bits_outputs = 0
    fsm_type = False #false:Moore true:Mealy

    #Methods
    def __init__(self):
        super().__init__()
        self.book = open(self.FSM_txt,'r',encoding='utf8')
        self.conf_file = open(self.conf,'r',encoding='utf8')
        self.states_names()
        self.in_out()
        self.input_val()
        self.fsm()
        self.config()
    
    def states_names(self):
        for line in self.book:
            match = re.findall(self.__pttrn_states,line)
            if(match): break
        self.states_string = match[0]
        self.states = re.split(r',|\s+',self.states_string)
        #print(self.states)
        #print(self.states_string)
        for line in self.book:
            match = re.findall(self.__pttrn_initial_state,line)
            if(match): break
        self.initial_state = match[0]
        self.num_bits_states = math.ceil(math.log(len(self.states),2))
        #print(self.initial_state)
        #print(self.num_bits_states)

    def in_out(self):
        for line in self.book:
            match_in = re.findall(self.__pttrn_inputs,line)
            if(match_in): break
        for line in self.book:
            match_out = re.findall(self.__pttrn_outputs,line)
            if(match_out): break
        pairs_in = re.split(r'\||\s+',match_in[0])
        pairs_out = re.split(r'\||\s+',match_out[0])
        for i in range(0,len(pairs_in)):
            split = re.split(',',pairs_in[i])
            if(split[0]=="clk" or split[0]=='reset'):
                split[0]+='_In'
                self.inputs.append(split[0])
            else:
                self.inputs.append(split[0])
            self.inputs_s.append(int(split[1]))
            if(i==len(pairs_in)-1):
                self.inputs_string += split[0]
            else:
                self.inputs_string+=split[0]+','
        for i in range(0,len(pairs_out)):
            split = re.split(',',pairs_out[i])
            if(split[0]=='clk' or split[0]=='reset'):
                split[0]+='_Out'
                self.outputs.append(split[0])
            else:
                self.outputs.append(split[0])
            self.outputs_s.append(int(split[1]))
            if(i==len(pairs_out)-1):
                self.outputs_string += split[0]
            else:
                self.outputs_string+=split[0]+','
        self.num_bits_inputs = sum(self.inputs_s)
        self.num_bits_outputs = sum(self.outputs_s)

    def input_val(self):
        for line in self.book:
            match = re.findall(self.__pttrn_in,line)
            if(match): break
        self.input_values = re.split(r',|\s+',match[0])
        #print(self.input_values)

    def fsm(self):
        for line in self.book:
            if(re.findall(self.__pttrn_fsm,line)):
                match=re.findall(self.__pttrn_fsm,line)
                split_states = re.split(',|\s',match[0][1])
                split_outputs = re.split(',|\s',match[0][2])
                self.next_state.update({match[0][0]:split_states})
                self.output_state.update({match[0][0]:split_outputs})
        if(len(self.output_state[self.initial_state])>1):
            self.fsm_type = True #Mealy
        #print(self.next_state)
        #print(self.output_state)
    
    def config(self):
        for line in self.conf_file:
            if(re.match(self.__pattern_timescale,line)):
                m = re.search(self.__pattern_timescale,line)
                self.timescale = m.group(1)
            elif(re.match(self.__pattern_delay,line)):
                m = re.search(self.__pattern_delay,line)
                self.delay = m.group(1)
            elif(re.match(self.__pattern_dumpvars,line)):
                m = re.search(self.__pattern_dumpvars,line)
                self.dumpvars = m.group(1)
            elif(re.match(self.__pattern_cases,line)):
                m = re.search(self.__pattern_cases,line)
                self.num_cases = int(m.group(1))
            elif(re.match(self.__pattern_periodclk,line)):
                m = re.search(self.__pattern_periodclk,line)
                self.period_clk = m.group(1)
            elif(re.match(self.__pattern_version,line)):
                m = re.search(self.__pattern_version,line)
                self.vers = int(m.group(1))
            elif(re.match(self.__pattern_clk,line)):
                m = re.search(self.__pattern_clk,line)
                self.clk = m.group(1)
            elif(re.match(self.__pattern_rst,line)):
                m = re.search(self.__pattern_rst,line)
                self.rst = m.group(1)
            elif(re.match(self.__pattern_c_state,line)):
                m = re.search(self.__pattern_c_state,line)
                self.c_state = m.group(1)
            elif(re.match(self.__pattern_n_state,line)):
                m = re.search(self.__pattern_n_state,line)
                self.n_state = m.group(1)
            elif(re.match(self.__pattern_edge,line)):
                m = re.search(self.__pattern_edge,line)
                self.edge = m.group(1)
            elif(re.match(self.__pattern_active_rst,line)):
                m = re.search(self.__pattern_active_rst,line)
                if(int(m.group(1)) == 1):
                    self.active_rst = True
                else:
                    self.active_rst = False
        self.conf_file.close()