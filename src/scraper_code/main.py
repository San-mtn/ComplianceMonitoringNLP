# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from io import BytesIO

import requests
from PyPDF2 import PdfReader, errors

from SearchMethod import GOVSR, Vlaanderen
import pandas as pd
import re


def prepare_govsr_df():
    govsr = GOVSR.GOVSR()
    govsrNames, govsrURLS = govsr.search()
    df = pd.DataFrame({'Organisation Name': govsrNames, 'Urls': govsrURLS})

    # Function to remove specific words
    def remove_words(name):
        words_to_remove = ['Jaarverslag', 'Jaarrekening', 'Concept', 'Rapportage', 'Interne']
        pattern = re.compile(r'\b(?:' + '|'.join(words_to_remove) + r')\b', re.IGNORECASE)
        return pattern.sub('', name).strip()

    # Function to remove 4-digit numbers and clean up
    def clean_numbers(name):
        name = re.sub(r'\b\d{4}\b', '', name)  # Remove 4-digit numbers
        name = name.replace('-', ' ').strip()  # Replace dashes with spaces and strip
        return re.sub(r'\s+', ' ', name)  # Remove extra spaces

    # Function to extract text between parentheses
    def extract_parentheses(name):
        match = re.search(r'\((.*?)\)', name)
        return match.group(1) if match else ''

    # Function to clean the 'Afkorting Uitgebreid' column
    def clean_name(name):
        return re.sub(r'\s*\(.*?\)\s*', '', name).strip()

    # Extract abbreviation and cleaned name
    df['Afkorting'] = df['Organisation Name'].apply(extract_parentheses)
    df['Afkorting Uitgebreid'] = df['Organisation Name'].apply(
        lambda x: clean_name(remove_words(clean_numbers(x))) if extract_parentheses(x) else '')

    # Update 'Organisation Name' with abbreviation if available
    df['Organisation Name'] = df.apply(lambda row: row['Afkorting'] if row['Afkorting'] else clean_name(
        remove_words(clean_numbers(row['Organisation Name']))), axis=1)

    # Drop 'Afkorting' column as it is now incorporated in 'Organisation Name'
    df.drop(columns=['Afkorting'], inplace=True)
    # Display the resulting DataFrame
    print(df.head())
    return df


def prepare_vlaanderen_df():
    vlaanderen = Vlaanderen.Vlaanderen()
    vlaanderen_names, vlaanderen_urls = vlaanderen.search()
    df = pd.DataFrame({'Organisation Name': vlaanderen_names, 'Urls': vlaanderen_urls})

    # Function to remove specific words
    def remove_words(name):
        words_to_remove = ['Jaarverslag', 'Jaarrekening', 'Concept', 'Rapportage', 'Interne']
        pattern = re.compile(r'\b(?:' + '|'.join(words_to_remove) + r')\b', re.IGNORECASE)
        return pattern.sub('', name).strip()

    # Function to remove 4-digit numbers and clean up
    def clean_numbers(name):
        name = re.sub(r'\b\d{4}\b', '', name)  # Remove 4-digit numbers
        name = name.replace('-', ' ').strip()  # Replace dashes with spaces and strip
        return re.sub(r'\s+', ' ', name)  # Remove extra spaces

    # Function to extract text between parentheses
    def extract_parentheses(name):
        match = re.search(r'\((.*?)\)', name)
        return match.group(1) if match else ''

    # Function to clean the 'Afkorting Uitgebreid' column
    def clean_name(name):
        return re.sub(r'\s*\(.*?\)\s*', '', name).strip()

    # Extract abbreviation and cleaned name
    df['Afkorting'] = df['Organisation Name'].apply(extract_parentheses)
    df['Afkorting Uitgebreid'] = df['Organisation Name'].apply(
        lambda x: clean_name(remove_words(clean_numbers(x))) if extract_parentheses(x) else '')

    # Update 'Organisation Name' with abbreviation if available
    df['Organisation Name'] = df.apply(lambda row: row['Afkorting'] if row['Afkorting'] else clean_name(
        remove_words(clean_numbers(row['Organisation Name']))), axis=1)

    # Drop 'Afkorting' column as it is now incorporated in 'Organisation Name'
    df.drop(columns=['Afkorting'], inplace=True)
    # Display the resulting DataFrame
    print(df.head())
    return df


def fill_5pages(df: pd.DataFrame):
    def get_5pages(url):
        try:
            print(url)
            text_of_first_5_pages = ''

            HTTPresponse = requests.get(url)
            # Create a BytesIO object from the PDF content
            bytes_stream = BytesIO(HTTPresponse.content)

            # Create a PdfReader object with the PDF content stream
            pdf_reader = PdfReader(bytes_stream)
            if pdf_reader:
                # Get the text from the first 5 pages
                text_of_first_5_pages = ''.join(page.extract_text() for page in pdf_reader.pages[:5])
            return text_of_first_5_pages
        except (requests.HTTPError, requests.ConnectionError, requests.exceptions.ChunkedEncodingError,
                requests.exceptions.RetryError, requests.exceptions.ContentDecodingError, requests.exceptions.SSLError,
                requests.exceptions.TooManyRedirects, requests.exceptions.SSLError, requests.exceptions.BaseHTTPError,
                requests.exceptions.ConnectTimeout, requests.exceptions.FileModeWarning,
                requests.exceptions.RequestException,
                errors.PdfReadError, errors.EmptyFileError, errors.PdfStreamError, errors.FileNotDecryptedError):
            return pd.NA


    df['Text'] = df['Urls'].apply(get_5pages)

    return df


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #df = fill_5pages(prepare_vlaanderen_df())
    #df = fill_5pages(prepare_govsr_df())
    #df.to_csv('vlaanderen_data.csv')

    # mix the two docs into one
    df1 = pd.read_csv('vlaanderen_data.csv')
    df2 = pd.read_csv('govsr_data.csv')
    df3 = pd.concat([df1, df2], ignore_index=True)
    df_cleaned = df3.drop(df3.columns[:1], axis=1)

    df_cleaned.to_csv('govsr+vlaanderen.csv')
    print(df1.head())
