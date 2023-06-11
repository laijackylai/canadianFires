import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from dateutil.parser import parse
import re
import spacy


def lemmatize(text):
    """
    Lemmatize a text using spaCy's lemmatizer.

    Args:
        text (str): The input text to lemmatize.

    Returns:
        str: The lemmatized form of the input text.
    """
    doc = nlp(text)
    lemmas = [token.lemma_ for token in doc]
    if len(lemmas) > 0:
        return lemmas[0]
    else:
        return ""


def parse_date(date_str):
    """
      Parse a date string into a standardized format "YYYY-MM-DD".

      Args:
          date_str (str): The date string to parse.

      Returns:
          str: The parsed date string in the format "YYYY-MM-DD" or None if parsing fails.
    """
    try:
        # Parse the date string using dateutil's parser
        parsed_date = parse(date_str)
        # Set the day component to 1
        parsed_date = parsed_date.replace(day=1)
        # Convert the parsed date to the desired format "YYYY-MM-DD"
        return parsed_date.strftime("%Y-%m-%d")
    except ValueError:
        return None


# Function to search the DataFrame


def search_dataframe_match_most(query, dataframe):
    """
    Search a dataframe for rows that match the most queries.

    Args:
        query (str): The search query.
        dataframe (pd.DataFrame): The dataframe to search.

    Returns:
        pd.DataFrame: Subset of the dataframe containing rows that match the most queries.
    """
    tokenized_query = word_tokenize(query)
    preprocessed_query = [
        lemmatize(word.lower()) for word in tokenized_query if word.lower() not in stop_words]
    print('query: ', preprocessed_query)
    search_results = dataframe
    result_counts = {}
    for word in preprocessed_query:
        matches = search_results[search_results['text'].str.contains(
            word, case=False)].index
        for match in matches:
            result_counts[match] = result_counts.get(match, 0) + 1
    if result_counts:
        max_count = max(result_counts.values())
        result_indices = [idx for idx,
                          count in result_counts.items() if count == max_count]
        return search_results.loc[result_indices, ['DATE', 'PROVINCE_CODE', 'MEAN_TEMPERATURE', 'CAUSE', 'SIZE_HA']]
    else:
        return pd.DataFrame(columns=['DATE', 'PROVINCE_CODE', 'MEAN_TEMPERATURE', 'CAUSE', 'SIZE_HA'])


def search_dataframe_match_all(query, dataframe):
    """
    Search a dataframe for rows that match all queries.

    Args:
        query (str): The search query.
        dataframe (pd.DataFrame): The dataframe to search.

    Returns:
        pd.DataFrame: Subset of the dataframe containing rows that match all queries.

    """
    tokenized_query = word_tokenize(query)
    preprocessed_query = [
        lemmatize(word.lower()) for word in tokenized_query if word.lower() not in stop_words]
    print('query: ', preprocessed_query)
    search_results = dataframe
    for word in preprocessed_query:
        search_results = search_results[search_results['text'].str.contains(
            word, case=False)]
    return search_results[['DATE', 'PROVINCE_CODE', 'MEAN_TEMPERATURE', 'CAUSE', 'SIZE_HA']]


def match_dates(uq):
    """
    Match and replace date patterns in a user query with parsed dates.

    Args:
        uq (str): The user query string.

    Returns:
        str: The user query string with matched dates replaced by parsed dates.
    """
    # Define a regular expression pattern to match dates
    date_patterns = [
        r'\d{4}-\d{2}',                              # YYYY-MM
        r'[A-Za-z]+\s+\d{4}',                         # Month YYYY
        r'[A-Za-z]{3}\s+\d{4}',                        # MMM YYYY
        r'[A-Za-z]{3}\.\s+\d{4}',                      # MMM. YYYY
    ]

    # Find all dates in the user query
    matches = []
    for pattern in date_patterns:
        matches += re.findall(pattern, uq)

    # Parse and replace the dates in the user query
    for match in matches:
        parsed_date = parse_date(match)
        if(parsed_date is None):
            continue
        else:
            uq = uq.replace(match, parsed_date)
    return uq


def check_province(uq, province_mapping):
    query_words = uq.split()
    for i, word in enumerate(query_words):
        if word in province_mapping:
            query_words[i] = province_mapping[word]
    uq = ' '.join(query_words)
    return uq


if __name__ == "__main__":
    # * setup
    # Load NLTK stopwords
    nltk.download('stopwords')
    nltk.download('wordnet')
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    nlp = spacy.load('en_core_web_sm')

    # Example DataFrame
    data = {
        'PROVINCE_CODE': ['AB', 'BC', 'AB', 'ON', 'BC'],
        'LOCAL_YEAR': [2020, 2020, 2021, 2022, 2022],
        'LOCAL_MONTH': [6, 7, 8, 9, 10],
        'MEAN_TEMPERATURE': [25.0, 28.5, 30.2, 22.7, 26.4],
        'CAUSE': ['Lightning', 'Human', 'Human', 'Lightning', 'Human'],
        'SIZE_HA': [100, 50, 200, 150, 75],
        'CHANCE_OF_FIRE': [0.8, 0.6, 0.9, 0.7, 0.5]
    }

    # * data preprocessing
    df = pd.DataFrame(data)

    province_mapping = {
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

    # Replace province codes with province names
    df['PROVINCE_CODE'] = [province_mapping[code]
                           for code in df['PROVINCE_CODE']]

    # Preprocess the dates
    df['LOCAL_YEAR'] = pd.to_numeric(
        df['LOCAL_YEAR'], errors='coerce')  # Convert to numeric
    df['LOCAL_MONTH'] = pd.to_numeric(
        df['LOCAL_MONTH'], errors='coerce')  # Convert to numeric

    # Convert month and year to datetime
    # Set default day value
    default_day = 1

    # Merge 'LOCAL_YEAR' and 'LOCAL_MONTH' into a single date column
    df['DATE'] = pd.to_datetime(df['LOCAL_YEAR'].astype(
        str) + '-' + df['LOCAL_MONTH'].astype(str) + '-' + str(default_day))

    # Drop unnecessary columns
    df.drop(['LOCAL_YEAR', 'LOCAL_MONTH'], axis=1, inplace=True)

    # Convert CAUSE column to lowercase
    df['CAUSE'] = df['CAUSE'].str.lower()

    # Text preprocessing using NLTK
    stop_words = set(stopwords.words('english'))

    # Preprocess the 'CAUSE' column
    df['CAUSE'] = df['CAUSE'].apply(lambda x: ' '.join(
        [word for word in word_tokenize(x) if word.lower() not in stop_words]))

    # Preprocess the DataFrame
    df['text'] = 'fire: date ' + df['DATE'].astype(str) + ' province code ' + df['PROVINCE_CODE'] + ' mean temperature ' + df['MEAN_TEMPERATURE'].astype(
        str) + ' cause ' + df['CAUSE'].astype(str) + ' size of fire in hectors ' + df['SIZE_HA'].astype(str) + ' chance of fire ' + df['CHANCE_OF_FIRE'].astype(str)
    df['text'] = df['text'].apply(lambda x: ' '.join(
        [word.lower() for word in word_tokenize(x)]))

    # * User input query
    user_query = input("Enter your search query: ")

    # * match dates
    user_query = match_dates(user_query)

    # * check for province mappings
    user_query = check_province(user_query, province_mapping)

    # * strategy: either absolute or optimistic
    strategy = "optimistic"

    if strategy == "optimistic":
        # Search the DataFrame
        results = search_dataframe_match_most(user_query, df)
    if strategy == "absolute":
        results = search_dataframe_match_all(user_query, df)

    # * Display the results
    if not results.empty:
        print("Search Results:")
        print(results)
    else:
        print("No results found.")
