import numpy as np
from helper_functions.get_healthcare_api_response import get_healthcare_api_response
from helper_functions.get_healthcare_api_labels import get_healthcare_api_labels
from tqdm.notebook import tqdm
import pandas as pd
import copy

acceptable_types = set(['drug', 'not_drug'])

def NER_maker(df, index): 
    s, d = get_healthcare_api_labels(df, index)
    
    entity_types = set([d[key]['entity_type'] for key in d])
    if len(entity_types&acceptable_types) == 0:
        return pd.DataFrame()
    word = []
    label = []
    ind = []
    for elem in s.split(): 
        ind.append(index)
        if elem in d: 
            word.append(elem.replace('#', ' '))
            label.append(d[elem]['entity_type'])
        else: 
            word.append(elem.replace('#', ' '))
            label.append('O')
    word.append(np.nan)
    label.append(np.nan)
    ind.append(index)
    temp = pd.DataFrame({
                         'word': word, 
                         'label': label, 
                         'orig_index': ind
                        })
    return temp

from concurrent.futures import ThreadPoolExecutor

NUM_THREADS = 10

def get_NER_format(df_input): 
    df = copy.deepcopy(df_input)
    df = df.reset_index().drop('index', axis = 1)
    pool = ThreadPoolExecutor(NUM_THREADS)

    def fun(x):
        try: 
            return NER_maker(df, x)
        except: 
            return pd.DataFrame()
    result = list(tqdm(pool.map(fun, list(df.index)), total=len(df.index)))
    
    df_final = pd.DataFrame()
    failed = []
    for i, elem in enumerate(result): 
        if len(elem) == 0: 
            failed.append(i)
        else:
            df_final = pd.concat([df_final, elem])

    return df_final, failed

