import re

def match_date(text):
    regex_pattern = r'(?P<date>\d{2}[-/]\d{4})|(?P<month_year>(?P<month>[A-Za-z]{3,})\.?\s\d{4})|(?P<year>\d{4})|(?P<month>[A-Za-z]{3,})'

    matched = []

    for match in re.finditer(regex_pattern, text):
        date = match.group('date')
        month_year = match.group('month_year')
        year = match.group('year')
        month = match.group('month')

        if date:
            matched.append(date)
        elif month_year:
            matched.append(month_year)
        elif year:
            matched.append(year)
        elif month:
            matched.append(month)

    return matched

if __name__ == "__main__":
    text = "This is a sample text with dates: 05/2022, May 2023, Jan. 2024, 2025, October, etc."

    matched_dates = match_date(text)
    print(matched_dates)
