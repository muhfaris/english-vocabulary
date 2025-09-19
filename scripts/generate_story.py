import argparse
import os
import sys
import datetime
import yaml
import csv
import random
import re
import glob

# Core Functions
# ---

def load_yaml_files_from_dir(directory):
    """Loads all YAML files from a directory and combines them into a single list."""
    data_list = []
    if not os.path.exists(directory):
        print(f"Warning: Directory not found, skipping: {directory}", file=sys.stderr)
        return data_list

    for filepath in glob.glob(os.path.join(directory, '*.yaml')) + glob.glob(os.path.join(directory, '*.yml')):
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                data = yaml.safe_load(f)
                if isinstance(data, list):
                    data_list.extend(data)
                else:
                    print(f"Warning: YAML file {filepath} does not contain a list. Skipping.", file=sys.stderr)
            except yaml.YAMLError as e:
                print(f"Warning: Could not parse {filepath}. Skipping. Error: {e}", file=sys.stderr)
    return data_list

def load_existing_vocab(csv_path="vocabularies.csv"):
    """Loads existing vocabulary from the CSV file into a set for fast lookups."""
    if not os.path.exists(csv_path):
        return set()

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            next(reader)  # Skip header
        except StopIteration:
            return set() # File is empty

        return {row[0].strip().lower() for row in reader if row}

def select_new_vocabulary(vocabulary_pool, story_template, existing_vocab):
    """Selects new vocabulary words that are not in the existing set."""
    new_words_pool = [
        v for v in vocabulary_pool
        if v['word'].lower() not in existing_vocab
    ]

    required_placeholders = {
        re.sub(r'[{}]', '', p) for p in re.findall(r'{\w+}', story_template)
    }

    selected_vocab = [
        v for v in new_words_pool if v.get('placeholder') in required_placeholders
    ]

    if len(selected_vocab) < len(required_placeholders):
        return None # Not enough words for this template

    return selected_vocab

def generate_kebab_case_title(text, num_words=4):
    """Generates a kebab-case title from the first few words of a text."""
    text = text.replace('**', '')
    words = re.findall(r'\b\w+\b', text.lower())
    return '-'.join(words[:num_words])

def generate_story_content(story_template, new_vocab_list):
    """Generates the story text, title, and highlighted words list."""
    vocab_map = {v['placeholder']: v['word'] for v in new_vocab_list}
    story_text = story_template.format(**vocab_map).strip()
    title = generate_kebab_case_title(story_text)
    highlighted_words = [v['word'] for v in new_vocab_list]

    story_data = {
        'title': title,
        'text': story_text,
        'highlighted_words': highlighted_words
    }
    return story_data

def update_story_yaml(story_data, date, stories_dir="stories"):
    """Creates the YAML file for the new story."""
    if not os.path.exists(stories_dir):
        os.makedirs(stories_dir)

    title = story_data['title']
    filepath = os.path.join(stories_dir, f"story-{title}.yaml")

    full_data = {
        'story': {
            'title': title,
            'date': date,
            'text': story_data['text'],
            'highlighted_words': story_data['highlighted_words']
        }
    }

    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(full_data, f, allow_unicode=True, sort_keys=False, indent=2)
    print(f"Successfully created story file: {filepath}")

def update_vocabulary_yaml(new_vocab_list, date, vocab_dir="vocabularies"):
    """Creates or appends to the vocabulary YAML file for the given date."""
    if not os.path.exists(vocab_dir):
        os.makedirs(vocab_dir)

    filepath = os.path.join(vocab_dir, f"vocabulary-from-story-{date}.yaml")

    existing_vocab_in_file = []
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                existing_vocab_in_file = yaml.safe_load(f) or []
                if not isinstance(existing_vocab_in_file, list):
                    print(f"Warning: Existing vocabulary file {filepath} is not a list. Overwriting.", file=sys.stderr)
                    existing_vocab_in_file = []
            except yaml.YAMLError as e:
                print(f"Warning: Could not parse {filepath}. Overwriting. Error: {e}", file=sys.stderr)
                existing_vocab_in_file = []

    existing_words_in_file = {v['word'] for v in existing_vocab_in_file}
    for new_vocab in new_vocab_list:
        if new_vocab['word'] not in existing_words_in_file:
            vocab_to_save = new_vocab.copy()
            vocab_to_save.pop('placeholder', None)
            existing_vocab_in_file.append(vocab_to_save)

    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(existing_vocab_in_file, f, allow_unicode=True, sort_keys=False, indent=2)
    print(f"Successfully updated vocabulary file: {filepath}")

def update_csv(filepath, header, rows):
    """Appends a list of rows to a CSV file."""
    file_exists = os.path.isfile(filepath)
    with open(filepath, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists or os.path.getsize(filepath) == 0:
            writer.writerow(header)
        writer.writerows(rows)

def main():
    parser = argparse.ArgumentParser(description="Generate a daily English story for a software developer.")
    parser.add_argument("date", help="The date for the story in YYYY-MM-DD format.")
    args = parser.parse_args()

    try:
        datetime.datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        print("Error: Date must be in YYYY-MM-DD format.", file=sys.stderr)
        sys.exit(1)

    # Load data from external files
    story_templates = load_yaml_files_from_dir('templates/stories')
    vocabulary_pool = load_yaml_files_from_dir('templates/vocabularies')

    if not story_templates:
        print("Error: No story templates found in 'templates/stories/'.", file=sys.stderr)
        sys.exit(1)
    if not vocabulary_pool:
        print("Error: No vocabulary pools found in 'templates/vocabularies/'.", file=sys.stderr)
        sys.exit(1)

    existing_vocab = load_existing_vocab()
    print(f"Loaded {len(existing_vocab)} existing vocabulary words.")

    # Find a template and a set of new words that work together
    random.shuffle(story_templates)
    selected_story_template = None
    new_vocab_list = None

    for template in story_templates:
        vocab_selection = select_new_vocabulary(vocabulary_pool, template, existing_vocab)
        if vocab_selection:
            selected_story_template = template
            new_vocab_list = vocab_selection
            break

    if not selected_story_template or not new_vocab_list:
        print("Error: Could not find a story template with enough new vocabulary words.", file=sys.stderr)
        sys.exit(1)

    print(f"Selected {len(new_vocab_list)} new words: {[v['word'] for v in new_vocab_list]}")

    story_content = generate_story_content(selected_story_template, new_vocab_list)
    story_content['date'] = args.date
    print(f"Generated story with title: '{story_content['title']}'")

    update_story_yaml(story_content, args.date)
    update_csv("stories.csv", ["title", "date"], [[story_content['title'], args.date]])
    print("Updated stories.csv")

    update_vocabulary_yaml(new_vocab_list, args.date)

    new_vocab_rows = [[v['word']] for v in new_vocab_list]
    update_csv("vocabularies.csv", ["Word"], new_vocab_rows)
    print("Updated vocabularies.csv")

    print(f"\nSuccessfully generated story and vocabulary for {args.date}")

if __name__ == "__main__":
    main()
