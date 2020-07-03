# os.urandom(16)
# random.uniform(2.5,22.5)
import pandas as pd
import numpy as np
from datetime import datetime
#import random
import os

from random import randint

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

input_table = pd.read_csv('C:/Users/H395978/AppData/Local/Programs/Thesis/stamm/test16digits.csv')
#output_table = pd.DataFrame()
output_dict = {}
for chunk in pd.read_csv('C:/Users/H395978/AppData/Local/Programs/Thesis/stamm/test16digits.csv',chunksize=5000):
    for index, row in chunk.iterrows():
        row['a'] = random_with_N_digits(16)
        row['b'] = random_with_N_digits(16)
        row['c'] = random_with_N_digits(16)
        row['d'] = random_with_N_digits(16)
        row['e'] = random_with_N_digits(16)
        row['f'] = random_with_N_digits(16)
        row['g'] = random_with_N_digits(16)
        row['h'] = random_with_N_digits(16)
        row['i'] = random_with_N_digits(16)
        row['j'] = random_with_N_digits(16)
        row['k'] = random_with_N_digits(16)
        row['l'] = random_with_N_digits(16)
        row['m'] = random_with_N_digits(16)
        row['n'] = random_with_N_digits(16)
        row['o'] = random_with_N_digits(16)
        row['p'] = random_with_N_digits(16)
        row['q'] = random_with_N_digits(16)
        row['r'] = random_with_N_digits(16)
        row['s'] = random_with_N_digits(16)
        row['t'] = random_with_N_digits(16)
        row['u'] = random_with_N_digits(16)
        row['v'] = random_with_N_digits(16)
        row['w'] = random_with_N_digits(16)
        row['x'] = random_with_N_digits(16)
        row['y'] = random_with_N_digits(16)
        row['z'] = random_with_N_digits(16)
        output_dict[index] = row
        print(index)

    output_table = pd.DataFrame.from_dict(output_dict, "index")
    print(output_table.head())
    output_dict = {}
    path=r'C:/Users/H395978/AppData/Local/Programs/Thesis/stamm/'
    # if file does not exist write header
    if not os.path.isfile(path+'16digit_gen_numbers.csv'):
        output_table.to_csv(path+'16digit_gen_numbers.csv',encoding='utf-8-sig',sep=',',index=False)
    else:
        output_table.to_csv(path+'16digit_gen_numbers.csv',encoding='utf-8-sig',sep=',',index=False,mode='a', header=False)





