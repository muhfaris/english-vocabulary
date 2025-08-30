import os
import yaml
from collections import Counter

def check_duplicate_vocabularies():
    words = []
    has_duplicates = False
    with open('vocabularies/vocabulary.yaml', 'r') as f:
        data = yaml.safe_load(f)
        if data:
            for entry in data:
                if 'word' in entry:
                    words.append(entry['word'])

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
    with open('stories/stories.yaml', 'r') as f:
        data = yaml.safe_load(f)
        if data:
            for story_item in data:
                if story_item and 'story' in story_item and 'title' in story_item['story']:
                    titles.append(story_item['story']['title'])

    title_counts = Counter(titles)
    duplicates = {title: count for title, count in title_counts.items() if count > 1}

    if duplicates:
        print("Duplicate stories found:")
        for title, count in duplicates.items():
            print(f"- '{title}' found {count} times.")
        has_duplicates = True

    return has_duplicates

if __name__ == "__main__":
    vocab_duplicates = check_duplicate_vocabularies()
    story_duplicates = check_duplicate_stories()

    if vocab_duplicates or story_duplicates:
        exit(1)
    else:
        print("No duplicates found.")
