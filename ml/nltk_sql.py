import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import spacy


def province_mapping(tokens):
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
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    lemmas = [token.lemma_ for token in doc]
    if len(lemmas) > 0:
        return lemmas[0]
    else:
        return ""
    
def parse_date(d):
    print(d)

def process_query(query):
    '''
    process query
    '''
    # Tokenization
    tokens = word_tokenize(query)

    # Province mapping
    tokens = province_mapping(tokens)

    tokens = [t.lower() for t in tokens]

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
                    parse_date(tmp_token)
            if token.startswith("cause") or token.startswith("by"):
                tmp_token, tmp_tag = t_tokens[index + 1]
                if tmp_token != "by":
                    cause = tmp_token
                else:
                    cause = t_tokens[index + 2][0]

        print(entity, time_word, from_year, from_month, to_year, to_month,  cause, location, table)                


    # Mapping to SQL
    # ... map the extracted information to SQL query components ...

    # SQL Query Generation
    # ... construct the SQL query string based on the mapped components ...

    # Return the SQL query
    return "sql_query"

if __name__ == "__main__":
    query = "give me fires in ON from 01-2014 to 02/2015 caused by lightning and after 09/2019"
        
    sql_query = process_query(query)
    # print(sql_query)
