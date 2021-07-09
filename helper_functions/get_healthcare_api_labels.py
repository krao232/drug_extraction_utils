from helper_functions.get_healthcare_api_response import get_healthcare_api_response
import copy

def find_word(index, sentence): 
    start = index
    end = index 
    while (sentence[start]!= ' ') and (start !=0): 
        start-=1
    while (sentence[end]!=' ') and (end != len(sentence)-1): 
        end+=1
    return sentence[start:end+1].strip()

def get_healthcare_api_labels(df_input, index):
    df = copy.deepcopy(df_input)
    sentence = df.sentence[index]
    dat = get_healthcare_api_response(sentence)
    for n in df.drugs[index]:   
        dat['result'][0]['entities'].append({'entities':[{'original_phrase': n[0]}], 
                                             'entity_type': n[1]})
        
    dic = {}
    for elem in dat['result'][0]['entities']:
        vals = elem['entities'][0]
        sentence = sentence.replace(vals['original_phrase'], vals['original_phrase'].replace(' ', '#'))
        key = find_word(sentence.find(vals['original_phrase'].replace(' ', '#')), sentence)
        dic[key] = {
            'entity_type': elem['entity_type'],
        }
    return sentence, dic