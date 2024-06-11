import numpy as np
import pandas as pd
from sys import argv
import re
import os
filename = 'input/temp.out'
def palindrome(filename):
      refine_data = []
      with open (filename, 'r') as f:
            lines = f.read().splitlines()
            print(lines[0])
            seq_name = lines.pop(0)
            p = re.compile(r'\w+\.\d+/\d+\-\d+')
            seq_name = p.search(seq_name).group()
            print(seq_name)
            #print(lines[0])
            data = [line.split() for line in lines]
            #print(len(data))
            
            refine_data = [d for d in data if d[0] != 'None' and float(d[0]) < 0]
            #print(refine_data[0]) 
            #print(refine_data)
            return seq_name, refine_data
print(palindrome(filename)[1])


#np_data = np.array(refine_data)
#df =pd.DataFrame(np_data)
#print(len(data))
#np_data = np.array(refine_data)
#print(len(refine_data))
#print(np_data)
#print(np_data.shape)
#print(df.info())

#p = np.array([[1,2,3,4],[5,6,7,8]])
#df = pd.DataFrame(p)
#p = np.append(p,[[9,10,11,12]],0)
#print(p.shape)
#print(p.size)
#print(df)
#print(p)

with open ('input/sample_RF01848.fa','r') as f1:
      sequences = f1.read().splitlines()
i = 0
temp_out = 'input/temp.out'
temp_fa = 'input/temp.fa'
data_dict = {}


def deal_single_seq(sequences):
      temp = sequences[i:i+2]
      seq = "\n".join(temp)
      print(seq)
      with open(temp_fa, 'w') as f:
            f.write(seq)
      os.system("~/transterm/2ndscore --no-rvs {} > {}".format(temp_fa, temp_out))

def get_data(filename):
      refine_data = []
      with open (filename, 'r') as f:
            lines = f.read().splitlines()     
            seq_name = lines.pop(0)
            p = re.compile(r'\w+\.\d+/\d+\-\d+')
            seq_name = p.search(seq_name).group()
            data = [line.split() for line in lines]
            refine_data = [d for d in data if d[0] != 'None' and float(d[0]) < 0]
      return seq_name, refine_data

def run(filename=argv[1],temp_fa='input/temp.fa',temp_out = 'input/temp.out'):
      result= {}
      with open (filename,'r') as f:
            sequences = f.read().splitlines()
      i = 0
      while i < len(sequences):
            deal_single_seq(sequences,i)
            (seq_name, refine_data) = palindrome(temp_out)
            result[seq_name] = refine_data
            
            i += 2


print(len(data_dict.values()))
      
