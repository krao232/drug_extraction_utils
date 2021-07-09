import pandas as pd
import copy

def drop_level(df):
    
    '''helper function to handle errors'''
    
    to_drop = []
    if 'level_0' in df.columns:
        to_drop.append('level_0')
    if 'level_1' in df.columns:
        to_drop.append('level_1')
    return df.drop(to_drop, axis = 1)

def sample_sentences_by(df, variables, N): 
    
    ''' helper function to sample sentence by a list of variables'''
    
    counts = df[variables+['sentence']].groupby(by = variables).count().reset_index()
    counts['sentence_count'] = counts.sentence
    counts = counts.drop('sentence', axis = 1)
    
    df1 = df.merge(counts, on= variables)
    df2 = df1[df1.sentence_count<N]
    df3 = df1[df1.sentence_count>=N]
    if len(df3)!=0:
        df4 = df3.groupby(by = variables, as_index = False).apply(pd.DataFrame.sample, n=N).reset_index()
        df5 = pd.concat([df2, df4]).reset_index().drop(['index', 'sentence_count'], axis = 1)   
    else: 
        df5 = df2.reset_index().drop(['index', 'sentence_count'], axis = 1)  
    return drop_level(df5)

def sample_binary(df, col, ratio):
    res = pd.DataFrame()
    for key in ratio:
        temp = df[df[col] == key].sample(n = ratio[key])
        res = pd.concat([res, temp]).reset_index().drop('index', axis = 1)
    return res
    

def process_sentences(df_input): 
    df = copy.deepcopy(df_input)
    #only get sentences from after September 15 2020
    df = df[df.date_epoch > 1600216444]
    #remove weird chars in sentence
    df['sentence'] = [n.replace('\n', '') for n in df.sentence]
    
    drugs_per_sentence = {}
    for drug, sentence, bert_class in df[['drug', 'sentence', 'bert_classification']].to_numpy():
        k, v = sentence, (drug, bert_class)
        if k in drugs_per_sentence: 
            if v not in drugs_per_sentence[k]: 
                drugs_per_sentence[k].append(v)
        else: 
            drugs_per_sentence[k] = [v]
    
    keep = df[['sentence']].drop_duplicates().index
    df = df[df.index.isin(keep)]
    
    df['drugs'] = [drugs_per_sentence[n] for n in df.sentence]
    
    #sample 10k sentences per company name 
    df = sample_sentences_by(df, ['company_name'], 10000)
    
    #sample 100 sentences by drug token
    df = sample_sentences_by(df, ['drug_token'], 100)
    
    #get 3:1 ratio of drug to not drug sentences
    df = sample_binary(df,'bert_classification', {'drug': 7500, 'not_drug': 2500})
    return df
    
    