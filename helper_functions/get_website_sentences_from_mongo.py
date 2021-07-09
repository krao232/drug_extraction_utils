import collections
import pandas as pd
import numpy as np
import nferx_py.utils as utils
from tqdm import tqdm_notebook as tqdm
import config


def get_website_sentences_from_mongo(N_sentences_per_extracted_entity = 1):

    collection = utils.get_mongo_collection_object('drug_extraction_media_corpus',
                                                   'modified_drug_extracted_sentences',
                                                   username= config.mongo_user, 
                                                   password= config.mongo_password)
    res = []
    count = 0 
    for n0 in tqdm(collection.find({}, 
                                 {'url': 1,
                                  'source':1,
                                  'drugs':1, 
                                  'company_name':1, 
                                  'date_generated_on': 1}),  total = 64132):
        if 'drugs' in n0: 
            for n1 in n0['drugs']: 
                if 'extracted_sentences' in n1: 
                    for n2 in n1['extracted_sentences']: 
                        count = 0
                        if 'source' in n2:
                            if n2['source'] == 'website_sentence': 
                                count+=1
                                if count<=N_sentences_per_extracted_entity:
                                    res.append({
                                                'drug_token': n1['token'],
                                                'drug': n1['matched_from'],
                                                'bert_classification': n1['bert_classification'],
                                                'sentence': n2['sentence'],
                                                'fda_approved': n1['fda_approved'], 
                                                'date_epoch': int(n0['date_generated_on']['epoch']),
                                                'date': n0['date_generated_on']['human_readable'],
                                                'source': n0['source'] if 'source' in n0 else None, 
                                                'mean': n1['mean'] if 'mean' in n1 else None,
                                                'company_name': n0['company_name'] if 'company_name' in n0 else None,
                                                'url': n0['url'] if 'url' in n0 else None
                                                }) 
                                    
    return pd.DataFrame(res)



