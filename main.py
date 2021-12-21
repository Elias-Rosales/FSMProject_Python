'''
Created on November, 2021
Authors:    Reyes Sánchez Luis Angel    
            Rivera Orozco David
            Rosales Galindo Elias
            Tacuapan Moctezuma Edgar
'''

import time
import os
from TBwrite import TBwrite
#from Design import Design

if __name__ == '__main__':
    start = time.time_ns()
    #HEADER PROGRAM
    print("*"*50)
    print("\nFSM DESIGNER")
    print('''
    Created on November 2021
    Authors:    Reyes Sánchez Luis Angel    
                Rivera Orozco David Gerardo
                Rosales Galindo Elías
                Tacuapan Moctezuma Edgar Ibis
    ''')
    print("*"*50)
    #------------------------------------------------------
    #START
    '''design'''
    #top = Design()
    '''testbench'''
    testbench = TBwrite()
    #END 
    end = time.time_ns()
    os.system("pause")
    print(f"Execution Time: {end-start} nsec")