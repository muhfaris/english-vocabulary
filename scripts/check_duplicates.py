import os
import yaml
from collections import Counter

def check_duplicate_vocabularies():
    words = []
    has_duplicates = False
    vocab_dir = 'vocabularies'
    for filename in os.listdir(vocab_dir):
        if filename.endswith('.yaml'):
            filepath = os.path.join(vocab_dir, filename)
            with open(filepath, 'r') as f:
                try:
                    data = yaml.safe_load(f)
                    if data:
                        for entry in data:
                            if isinstance(entry, dict) and 'word' in entry:
                                words.append(entry['word'])
                except yaml.YAMLError as e:
                    print(f"Error parsing {filepath}: {e}")

    word_counts = Counter(words)
    duplicates = {word: count for word, count in word_counts.items() if count > 1}

    if duplicates:
        print("Duplicate vocabularies found:")
        for word, count in duplicates.items():
            print(f"- '{word}' found {count} times.")
        has_duplicates = True

    return has_duplicates

def check_duplicate_stories():
    titles = []
    has_duplicates = False
    stories_dir = 'stories'
    for filename in os.listdir(stories_dir):
        if filename.endswith('.yaml'):
            filepath = os.path.join(stories_dir, filename)
            with open(filepath, 'r') as f:
                try:
                    data = yaml.safe_load(f)
                    if data and isinstance(data, dict) and 'story' in data and 'title' in data['story']:
                        titles.append(data['story']['title'])
                except yaml.YAMLError as e:
                    print(f"Error parsing {filepath}: {e}")

    title_counts = Counter(titles)
    duplicates = {title: count for title, count in title_counts.items() if count > 1}

    if duplicates:
        print("Duplicate stories found:")
        for title, count in duplicates.items():
            print(f"- '{title}' found {count} times.")
        has_duplicates = True

    return has_duplicates

if __name__ == "__main__":
    print("Checking for duplicate vocabulary words...")
    vocab_duplicates = check_duplicate_vocabularies()

    print("\nChecking for duplicate story titles...")
    story_duplicates = check_duplicate_stories()

    if vocab_duplicates or story_duplicates:
        print("\nDuplicate entries found. The check has failed.")
        exit(1)
    else:
        print("\nNo duplicates found in vocabularies or stories.")
