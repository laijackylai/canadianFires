import re
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import spacy
import gensim
from nltk.corpus import stopwords
import csv

# nltk.download('brown')
# model = gensim.models.Word2Vec(brown.sents())
# model.save('brown.embedding')
# exit()

nlp = spacy.load('en_core_web_lg')
# model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True)

def match_reason(text):
    '''
    match reason words
    '''
    reason_words = []
    with open('reason_words.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            reason_words.extend(row)
    reason_words = [word.lower() for word in reason_words]
    tokens = word_tokenize(text.lower())
    matches = [token for token in tokens if token in reason_words]
    return matches

def province_mapping(tokens):
    '''
    map provinces shorthands and full names
    '''
    province_mappings = {
        'AB': 'Alberta',
        'BC': 'British Columbia',
        'MB': 'Manitoba',
        'NB': 'New Brunswick',
        'NL': 'Newfoundland and Labrador',
        'NS': 'Nova Scotia',
        'NT': 'Northwest Territories',
        'NU': 'Nunavut',
        'ON': 'Ontario',
        'PE': 'Prince Edward Island',
        'QC': 'Quebec',
        'SK': 'Saskatchewan',
        'YT': 'Yukon'
    }

    for i, t in enumerate(tokens):
        new_t = province_mappings.get(t)
        if new_t:
            tokens[i] = new_t

    return tokens

def lemmatize(text):
    """
    Lemmatize a text using spaCy's lemmatizer.
    """
    doc = nlp(text)
    lemmas = [token.lemma_ for token in doc]
    if len(lemmas) > 0:
        return lemmas[0]
    else:
        return ""
    
def most_similar(word, topn=5):
    try:
        top_similar_words = model.most_similar(positive=[word], topn = topn) 
        text_words = [word for word, _ in top_similar_words]
        return text_words 
    except Exception:
        return []

def process_query(query):
    '''
    process query
    '''
    # Tokenization
    tokens = word_tokenize(query)

    # Province mapping
    tokens = province_mapping(tokens)

    tokens = [lemmatize(t.lower()) for t in tokens]

    # POS Tagging
    tagged_tokens = pos_tag(tokens)
    
    split_tokens = []
    temp_tokens = []

    for index, (token, tag) in enumerate(tagged_tokens):
        if tag == "CC":
            if temp_tokens:
                split_tokens.append(temp_tokens)
                temp_tokens = []
        else:
            temp_tokens.append((token, tag))
    if temp_tokens:
        split_tokens.append(temp_tokens)

    # Query Parsing
    for t_tokens in split_tokens:
        entity = "*"
        time_word = "*"
        from_year = "*"
        from_month = "*"
        to_year = "*"
        to_month = "*"
        cause = "*"
        location = "*"
        table = "nltk"

        for index, (token, tag) in enumerate(t_tokens):
            print(index, token, tag)
            if tag.startswith("IN"):
                tmp_token, tmp_tag = t_tokens[index + 1]
                if tmp_tag.startswith("NN"): # local
                    location = tmp_token
            if tag.startswith("IN") or tag.startswith("TO"):
                tmp_token, tmp_tag = t_tokens[index + 1]
                if tmp_tag.startswith("CD"): # time
                    time_word = token
                    # parse time
                    matches = re.findall(r'\d{2}/\d{4}|\d{4}', tmp_token)
                    if len(matches) > 0:
                        match = matches[0]
                        if '/' in match: # mm/yyyy
                            year = match.split('/')[1]
                            month =  match.split('/')[0]
                            if from_year == '*':
                                from_year = year
                            else:
                                to_year = year
                            if from_month == '*':
                                from_month = month
                            else:
                                to_month = month
                        else: # yyyy
                            if from_year == '*':
                                from_year = match
                            else:
                                to_year = match
            reasons = match_reason(token)
            print(reasons)
            if len(reasons) > 0:
                tmp_token, tmp_tag = t_tokens[index + 1]
                if tmp_token != "by":
                    cause = tmp_token
                else:
                    cause = t_tokens[index + 2][0]

        print(entity, time_word, from_year, from_month, to_year, to_month,  cause, location, table, '\n')                


    # Mapping to SQL
    # ... map the extracted information to SQL query components ...

    # SQL Query Generation
    # ... construct the SQL query string based on the mapped components ...

    # Return the SQL query
    return "sql_query"

if __name__ == "__main__":
    #! assuming dates are always correctly formatted in mm/yyyy or yyyy
    query = "give me fires in ON from 01/2014 to 02/2015 caused by lightning and after 2019 because of humans or due to fire"
        
    sql_query = process_query(query)
    # print(sql_query)
