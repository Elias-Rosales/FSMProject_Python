#TESTBENCH WRITTER
from Design import Design
import re
from os import getcwd

class TBwrite(Design):
    #Attributes
    TB = None
    instantiated_modules = []
    num_mod = None
    #Methods
    def __init__(self):
        super().__init__()
        self.TB = open(self.TestB,'w',encoding='utf8')
        self.Header()
        self.In_Out()
        self.DUT()
        self.crate_path()
        self.Initial_Begin()
        self.DirTB()
    
    def Header(self):
        self.num_mod = len(self.instantiated_modules)
        self.TB.write("`timescale %s\n" %self.timescale)               # write timescale
        if(self.num_mod!=0):                                           # if there are instantiated modules
            for i in range(0,self.num_mod):
                self.TB.write('`include "%s.sv"\n' %self.instantiated_modules[i]) # if so, include them
        self.TB.write("\nmodule %s_TB();\n" %self.module_name)           # write module_name_TB;

    # Write inputs and outputs inputs_s,inputs,outputs_s,outputs
    def In_Out(self):
        _inputs=[[] for x in range(max(self.inputs_s))]          # list of lists of max bit size value
        # write Inputs
        for j in range(0,len(self.inputs)):
            _inputs[self.inputs_s[j]-1].append(self.inputs[j])
        for i in range(0,len(_inputs)):
            if (_inputs[i]):
                if i+1 == 1:
                    self.TB.write("\treg %s, %s, " %(self.clk,self.rst))
                    for j in range(0,len(_inputs[i])):
                        if(j == len(_inputs[i])-1):
                            self.TB.write("%s_TB;\n" %_inputs[i][j])
                            break
                        self.TB.write("%s_TB, " %_inputs[i][j])
                else:
                    self.TB.write("\treg [%i:0] " %i)
                    for j in range(0,len(_inputs[i])):
                        if(j == len(_inputs[i])-1):
                            self.TB.write("%s_TB;\n" %_inputs[i][j])
                            break
                        self.TB.write("%s_TB, " %_inputs[i][j])
        # Write outputs
        _outputs=[[] for x in range(max(self.outputs_s))]         # list of lists of max bit size value
        for j in range(0,len(self.outputs)):
            _outputs[self.outputs_s[j]-1].append(self.outputs[j])
        for i in range(0,len(_outputs)):
            if (_outputs[i]):
                if i+1 == 1:
                    self.TB.write("\twire ")
                    for j in range(0,len(_outputs[i])):
                        if(j == len(_outputs[i])-1):
                            self.TB.write("%s_TB;\n" %_outputs[i][j])
                            break
                        self.TB.write("%s_TB, " %_outputs[i][j])
                else:
                    self.TB.write("\twire [%i:0] " %i)
                    for j in range(0,len(_outputs[i])):
                        if(j == len(_outputs[i])-1):
                            self.TB.write("%s_TB;\n" %_outputs[i][j])
                            break
                        self.TB.write("%s_TB, " %_outputs[i][j])
    
    # Write device under test
    def DUT(self):
        self.flag1 = False
        self.flag2 = False
        self.num_in = len(self.inputs)
        self.num_out = len(self.outputs)
        self.TB.write("\n\t%s DUT(.%s(%s), .%s(%s), " %(self.module_name,self.clk,self.clk,self.rst,self.rst))               # initiate DUT
        if(self.num_in!=0):                                            # check if there are inputs
            for i in range(0,self.num_in):
                if(i==self.num_in-1):                                  # if it is the last input
                    if(self.num_out!=0):                               # if there are outputs, finish with ,\n
                        self.TB.write(".%s(%s_TB),\n" %(self.inputs[i],self.inputs[i]))
                        break
                    else:                                              # if there are no outputs, finish line with );
                        self.TB.write(".%s(%s_TB));\n" %(self.inputs[i],self.inputs[i])) 
                else:
                    self.TB.write(".%s(%s_TB), " %(self.inputs[i],self.inputs[i]))
        else:
            self.flag1 = True                                          # if there are no inputs flag1 = true
        if(self.num_out!=0):                                           # check if there are outputs
            self.TB.write('\t\t')
            for i in range(0,self.num_out):
                if(i==self.num_out-1):                                 # if it is the last output, finish line with );
                    self.TB.write(".%s(%s_TB));\n" %(self.outputs[i],self.outputs[i]))  
                else:                                                  # else, keep writing outputs
                    self.TB.write(".%s(%s_TB), " %(self.outputs[i],self.outputs[i]))    
        else:
            self.flag2 = True                                          # if there are no outputs flag2 = True
        if(self.flag1 and self.flag2):                                 # if no inputs and no outputs, then write );\n for the DUT
            self.TB.write(");\n")

    # Create stimuli
    def crate_path(self):
        stack = [self.initial_state]  # Stack type structure
        base = [self.initial_state]
        statesArray = [self.initial_state]
        path_traveled = []
        targets = []
        while len(stack) > 0:
            actual = stack.pop()
            statesPossibilites = self.next_state[actual]
            path_traveled.append(actual)
            i = 0
            for v in statesPossibilites:
                if v not in statesArray:
                    statesArray.append(v)
                    stack.append(v)
                    base.append(actual)
                else:
                    i += 1
            if i == len(statesPossibilites):
                targets.append(actual)
        #print("targets",targets)
        # Paths
        paths = {}
        for i in targets:
            _path = [i]
            tempo = i
            while tempo != self.initial_state:
                element = statesArray.index(tempo)
                tempo = base[element]
                _path.insert(0,tempo)
            paths[i] = _path
            #print(f"ruta {i}: {paths[i]}")
        # Stimuli
        stimuli = [] 
        for key in paths:
            stimulus = []
            list = paths[key]
            actual = list[0]
            statesPossibilites = self.next_state[actual]
            for i in range(len(list)-1):
                nextStateEvaluate = list[i+1]
                stimulus.append(statesPossibilites.index(nextStateEvaluate)) 
                statesPossibilites = self.next_state[nextStateEvaluate]
            stimuli.append(stimulus) 
        #print(stimuli)
        self.stimuli = stimuli

    # Write initial begin and stimuli
    def Initial_Begin(self):
        self.TB.write("\n\tinitial begin\n\t\t%s = 1'b0;\n\t\t%s = 1'b1;\n\tend\n" %(self.clk,self.rst))
        self.TB.write("\n\talways begin %s = ~ %s; %s; end\n" %(self.clk, self.clk,self.period_clk))
        self.TB.write("\n\tinitial begin\n\t\t$dumpfile(\"%s.vcd\");\n" %(self.module_name))
        self.TB.write("\t\t$dumpvars(%s,%s_TB);\n\n" %(self.dumpvars,self.module_name))

        num_bits = sum(self.inputs_s)                          # num of input bits
        in_vector = ''
        if(not self.flag1):                                           # if there are inputs
            for i in range(0,self.num_in):                            # write inputs vector and bit vector
                if(i==self.num_in-1):                                 # if is the last input
                    in_vector = in_vector+'%s_TB' %(self.inputs[i]) # write only input
                else:
                    in_vector = in_vector+'%s_TB,' %(self.inputs[i])    #else, write a comma
            self.TB.write("\t\t{%s} = %i'b%s; %s\n" %(in_vector,num_bits,f'{0:0{num_bits}b}',self.period_clk))
            self.TB.write("\t\t%s = 1'b0; %s\n" %(self.rst,self.delay))
            for i in range(len(self.stimuli)):
                tempo = self.stimuli[i]
                for j in range(len(tempo)):
                    self.TB.write("\t\t{%s} = %i'b%s; %s\n" %(in_vector,num_bits,f'{tempo[j]:0{num_bits}b}',self.delay))
                if i < len(self.stimuli)-1:
                    self.TB.write("\t\t%s = 1'b1; %s\n" %(self.rst,self.delay))
                    self.TB.write("\t\t%s = 1'b0; %s\n" %(self.rst,self.delay))
        self.TB.write('\n\t\t$finish;\n')
        self.TB.write('\tend')
        self.TB.write("\nendmodule")
        self.TB.close()

    def DirTB(self):
        if(re.match(re.compile(r'^[C|c]:.*[\\\/](\w+.sv)$'),self.TestB)):
            print(f"[Testbench File]: {self.TestB}\n")
        else:
            print(f"[Testbench File]: {getcwd()}\\{self.TestB}\n")