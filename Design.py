#DESIGN CLASS
from sys import path
from ReadData import ReadData
from os import dup
from os import getcwd
import re
class Design(ReadData):
    #properties
    Design_F = None
    name = ""
    path = ""
    module_name = None
    #Member Functions
    def __init__(self):
        super().__init__()
        if(self.design):
            self.name = self.design
            self.path = self.design_path
        else:
            self.name = self.FSM
            self.path = self.FSM_path
        self.Design_F = open(self.path,'w',encoding="utf8")
        self.module_name = self.name.replace('.sv','')
        self.module()
        self.inputs_print()
        self.outputs_print()
        self.States()
        self.StateReg()
        self.NextStateLogic()
        self.OutputLogic()
        self.Dir()

    def module(self):
        if(self.vers == 0):
            self.Design_F.write("module %s(%s,%s," %(self.module_name,self.clk,self.rst))
            for i in self.inputs:                   #Printing of inputs into module declaration
                self.Design_F.write("%s," %i)
            for i in self.outputs:                  #Printing of outputs into mudole declaration 
                if (i != self.outputs[-1]):
                    self.Design_F.write("%s," %i)
                else:
                    self.Design_F.write("%s);\n" %i)
        else:
            self.Design_F.write("module %s(\n" %self.module_name)
    
    def inputs_print(self):
        #inputs
        inp = {}
        for x in self.inputs_s:
            inp[x] = []   
        for key in inp:
            for i in range(0,len(self.inputs_s)):
                if(key==self.inputs_s[i]):
                    inp[key].append(self.inputs[i])
            if(key == 1):
                self.Design_F.write("\tinput %s,%s,"%(self.clk,self.rst))
            else:
                self.Design_F.write("\tinput [%i:0] " %key)
            for i in inp[key]:
                if(i == inp[key][-1] and self.vers == 0):
                    self.Design_F.write("%s;\n" %i)
                    break
                if(i == inp[key][-1] and self.vers == 1):
                    self.Design_F.write("%s,\n" %i)
                    break
                self.Design_F.write("%s," %i)

    def outputs_print(self):
        #outputs
        out = {}
        temp_out =[]
        for x in self.outputs_s:
            out[x] = []
        for key in out:
            temp_out.append(key)
        for key in out:
            for i in range(0,len(self.outputs_s)):
                if(key==self.outputs_s[i]):
                    out[key].append(self.outputs[i])
            if(key == 1):
                self.Design_F.write("\toutput reg ")
            else:
                self.Design_F.write("\toutput reg [%i:0] " %key)
            for i in out[key]:
                if(i==out[key][-1] and self.vers == 0):
                    self.Design_F.write("%s;\n" %i)
                    break
                if(i==out[key][-1] and self.vers == 1):
                    if(len(out.keys()) != 1 and key!=temp_out[-1]):
                        self.Design_F.write("%s,\n" %i)
                        break
                    else:
                        self.Design_F.write("%s);\n" %i)
                        break
                self.Design_F.write("%s," %i)
        self.Design_F.write("\n")
        
    def States(self):
        self.Design_F.write(f"\treg [{self.num_bits_states-1}:0] {self.c_state};\n")
        self.Design_F.write(f"\treg [{self.num_bits_states-1}:0] {self.n_state};\n\n")
        for i in range(0,len(self.states)):
            self.Design_F.write("\tparameter %s = %d;\n" %(self.states[i],i))
        self.Design_F.write("\n")
        self.Design_F.write("\tinitial begin\n")
        self.Design_F.write("\t\t%s = %s;\n"%(self.c_state,self.initial_state))
        self.Design_F.write("\tend\n")
        self.Design_F.write("\n")
    
    def StateReg(self):
        self.Design_F.write("\talways @(%s %s, %s %s)\n"%(self.edge,self.clk,self.edge,self.rst))
        self.Design_F.write("\t\tbegin\n")
        self.Design_F.write("\t\t\tif (")
        if (not self.active_rst):
            self.Design_F.write("~")
        self.Design_F.write("%s)\n"%self.rst) #verificar activo en l o h
        self.Design_F.write("\t\t\t\t%s <= %s;\n"%(self.c_state,self.initial_state))
        self.Design_F.write("\t\t\telse\n")
        self.Design_F.write("\t\t\t\t%s <= %s;\n"%(self.c_state,self.n_state))
        self.Design_F.write("\t\tend\n")
        self.Design_F.write("\n")
    
    def NextStateLogic(self):
        self.Design_F.write("//Next state logic\n")
        self.Design_F.write("\talways @(%s,%s)\n"%(self.c_state,self.inputs_string))
        self.Design_F.write("\t\tbegin\n")
        #begin
        self.Design_F.write("\t\t\tcase(%s)"%self.c_state)
        #begin
        last_index=len(self.next_state[self.initial_state])-1
        for i in range(len(self.states)):
            if(i<len(self.states)-1):
                self.Design_F.write('\n\t\t\t\t%s: '%self.states[i])
            else:
                self.Design_F.write('\n\t\t\t\tdefault: ')
            #entramos a states[i]
            if(self.num_bits_inputs>1):
                self.Design_F.write('\n\t\t\t\t\tcase({'+self.inputs_string+'})')
                seen=set()
                duplicates={}
                printed=set()
                var=''
                for x in self.next_state[self.states[i]]:
                    if x not in seen:
                        seen.add(x)
                    else:
                        duplicates[x] = [j for j,n in enumerate(self.next_state[self.states[i]]) if n == x]
                #print(duplicates)
                for x in self.next_state[self.states[i]]:
                    flag_default=False
                    if x in duplicates and x not in printed:
                        for k in range(len(duplicates[x])):
                            for m in duplicates[x]: 
                                if (m == last_index):
                                    flag_default = True
                            if(flag_default):
                                var = "\n\t\t\t\t\t\tdefault: next_state = "+x+";"
                            else:
                                if(k<len(duplicates[x])-1):
                                    var += "\n\t\t\t\t\t\t%i'b%s,\n"%(self.num_bits_inputs,self.input_values[duplicates[x][k]])
                                else:
                                    var += "\t\t\t\t\t\t%i'b%s: next_state = %s;"%(self.num_bits_inputs,self.input_values[duplicates[x][k]],x)
                        self.Design_F.write(var)
                        var=''
                        printed.add(x)
                    elif x not in duplicates:
                        if(self.next_state[self.states[i]].index(x)==last_index):
                            flag_default = True
                        if(flag_default):
                            var = "\n\t\t\t\t\t\tdefault: next_state = "+x+";"
                        else:
                            var = "\n\t\t\t\t\t\t%i'b%s: next_state = %s;"%(self.num_bits_inputs,self.input_values[self.next_state[self.states[i]].index(x)],x)
                        self.Design_F.write(var)
                self.Design_F.write("\n\t\t\t\t\tendcase")
            else:
                if(self.input_values[0]=='0'):
                    if(self.next_state[self.states[i]][1] == self.next_state[self.states[i]][0]):
                        self.Design_F.write('\n          next_state = %s;'%self.next_state[self.states[i]][1])
                    else:
                        self.Design_F.write('\n          if('+self.inputs_string+')')
                        self.Design_F.write('\n            next_state = %s;'%self.next_state[self.states[i]][1])
                        self.Design_F.write('\n          else')
                        self.Design_F.write('\n            next_state = %s;'%self.next_state[self.states[i]][0])
                else:
                    if(self.next_state[self.states[i]][1] == self.next_state[self.states[i]][0]):
                        self.Design_F.write('\n          next_state = %s;'%self.next_state[self.states[i]][1])
                    else:
                        self.Design_F.write('\n          if('+self.inputs_string+')')
                        self.Design_F.write('\n            next_state = %s;'%self.next_state[self.states[i]][0])
                        self.Design_F.write('\n          else')
                        self.Design_F.write('\n            next_state = %s;'%self.next_state[self.states[i]][1])
        #end
        self.Design_F.write("\n\t\t\tendcase\n")
        self.Design_F.write("\t\tend\n")
        self.Design_F.write("\n")

    def OutputLogic(self):
        self.Design_F.write("//Output Logic\n")
        if(self.num_bits_outputs>1):
            self.outputs_string = '{'+self.outputs_string+'}'
        if(self.fsm_type): #True = Mealy, False = Moore
            self.Design_F.write("\talways @(%s"%self.c_state)
            self.Design_F.write(",%s)\n"%self.inputs_string)
            self.Design_F.write("\t\tbegin\n")
            self.Design_F.write("\t\t\tcase(%s)"%self.c_state)
            last_index = len(self.output_state[self.initial_state])-1
            for i in range(len(self.states)):
                if(i<len(self.states)-1):
                    self.Design_F.write('\n\t\t\t\t%s: '%self.states[i])
                else:
                    self.Design_F.write('\n\t\t\t\tdefault: ')
                if(self.num_bits_inputs>1):
                    self.Design_F.write('\n\t\t\t\t\tcase({'+self.inputs_string+'})')
                    seen=set()
                    duplicates={}
                    printed=set()
                    var=''
                    for x in self.output_state[self.states[i]]:
                        if x not in seen:
                            seen.add(x)
                        else:
                            duplicates[x] = [j for j,n in enumerate(self.output_state[self.states[i]]) if n==x]
                    for x in self.output_state[self.states[i]]:
                        flag_default=False
                        if x in duplicates and x not in printed:
                            for k in range(len(duplicates[x])):
                                for m in duplicates[x]:
                                    if(m==last_index):
                                        flag_default=True
                                if(flag_default):
                                    var="\n\t\t\t\t\t\tdefault: %s = %i'b%s;"%(self.outputs_string,self.num_bits_outputs,x)
                                else:
                                    if(k<len(duplicates[x])-1):
                                        var+="\n\t\t\t\t\t\t%i'b%s,\n"%(self.num_bits_inputs,self.input_values[duplicates[x][k]])
                                    else:
                                        var+="\t\t\t\t\t\t%i'b%s: %s = %i'b%s;"%(self.num_bits_inputs,self.input_values[duplicates[x][k]],self.outputs_string,self.num_bits_outputs,x)
                            self.Design_F.write(var)
                            var=''
                            printed.add(x)
                        elif x not in duplicates:
                            if(self.output_state[self.states[i]].index(x)==last_index):
                                flag_default = True
                            if(flag_default):
                                var="\n\t\t\t\t\t\tdefault: "+self.outputs_string+" = "+str(self.num_bits_outputs)+"'b"+x+";"
                            else:
                                var="\n\t\t\t\t\t\t%i'b%s: %s = %i'b%s;"%(self.num_bits_inputs,self.input_values[self.output_state[self.states[i]].index(x)],self.outputs_string,self.num_bits_outputs,x)
                            self.Design_F.write(var)
                    self.Design_F.write("\n\t\t\t\t\tendcase")
                else:
                    if(self.input_values[0]=='0'):
                        if(self.output_state[self.states[i]][1] == self.output_state[self.states[i]][0]):
                            self.Design_F.write("\n          %s = %i'b%s;"%(self.outputs_string,self.num_bits_outputs,self.output_state[self.states[i]][1]))
                        else:
                            self.Design_F.write('\n          if('+self.inputs_string+')')
                            self.Design_F.write("\n            %s = %i'b%s;"%(self.outputs_string,self.num_bits_outputs,self.output_state[self.states[i]][1]))
                            self.Design_F.write('\n          else')
                            self.Design_F.write("\n            %s = %i'b%s;"%(self.outputs_string,self.num_bits_outputs,self.output_state[self.states[i]][0]))
                    else:
                        if(self.output_state[self.states[i]][1] == self.output_state[self.states[i]][0]):
                            self.Design_F.write("\n          %s = %i'b%s;"%(self.outputs_string,self.num_bits_outputs,self.output_state[self.states[i]][1]))
                        else:
                            self.Design_F.write('\n          if('+self.inputs_string+')')
                            self.Design_F.write("\n            %s = %i'b%s;"%(self.outputs_string,self.num_bits_outputs,self.output_state[self.states[i]][0]))
                            self.Design_F.write('\n          else')
                            self.Design_F.write("\n            %s = %i'b%s;"%(self.outputs_string,self.num_bits_outputs,self.output_state[self.states[i]][1]))
            self.Design_F.write("\n\t\t\tendcase\n")
            self.Design_F.write("\t\tend\n")
            #print("mealy")
        else:
            self.Design_F.write("\talways @(%s)\n"%self.c_state)
            self.Design_F.write("\t\tbegin\n")
            self.Design_F.write("\t\t\tcase(%s)"%self.c_state)
            for key,value in self.output_state.items():
                if(key!=list(self.output_state.keys())[-1]):
                    if(len(self.outputs)>1):
                        self.Design_F.write("\n\t\t\t\t%s: %s = %i'b%s;"%(key,self.outputs_string,self.num_bits_outputs,value[0]))
                    else:
                        self.Design_F.write("\n\t\t\t\t%s: %s = %i'b%s;"%(key,self.outputs_string,self.num_bits_outputs,value[0]))
                else:
                    self.Design_F.write("\n\t\t\t\tdefault: %s = %i'b%s;"%(self.outputs_string,self.num_bits_outputs,value[0]))
            self.Design_F.write("\n\t\t\tendcase\n")
            self.Design_F.write("\t\tend\n")
            #print("moore")
        self.Design_F.write("endmodule")
        self.Design_F.close()

    def Dir(self):
        if(re.match(re.compile(r'^[a-zA-Z.].*[\\\/](\w+.sv)$'),self.path)):
            print(f"[Design File]: {self.path}")
        else:
            print(f"[Design File]: {getcwd()}\\{self.path}")