import argparse
import requests
from collections import Counter
import os

def read_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return None

def download_file(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error downloading the file: {e}")
        return None

def word_count(content):
    return sum(1 for word in content.split())

def letter_count(content):
    return {char: count for char, count in Counter(content.lower()).items() if char.isalpha()}

def main(input_path):
    if os.path.isfile(input_path):
        content = read_file(input_path)
    else:
        content = download_file(input_path)
    
    if content is None:
        print("File not found or unable to download. Please check the file path or URL.")
        return
    
    words = word_count(content)
    letters = letter_count(content)

    print(f"--- Begin report of {input_path} ---")
    print(f"{words} words found in the document\n")
    
    sorted_letters = sorted(letters.items(), key=lambda item: item[1], reverse=True)
    for letter, count in sorted_letters:
        print(f"The '{letter}' character was found {count} times")
    
    print("--- End report ---")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Count words and letters in a text file or from a URL.")
    parser.add_argument('input_path', type=str, help='Path to the text file or URL of the text file')
    args = parser.parse_args()
    main(args.input_path)
