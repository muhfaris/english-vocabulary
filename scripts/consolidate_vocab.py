import os
import yaml

def consolidate_vocabularies():
    all_words = {}
    for filename in os.listdir('vocabularies'):
        if filename.endswith('.yaml'):
            with open(os.path.join('vocabularies', filename), 'r') as f:
                data = yaml.safe_load(f)
                if data:
                    for entry in data:
                        if 'word' in entry:
                            word = entry['word']
                            if word not in all_words:
                                all_words[word] = entry

    # Sort by word for consistency
    sorted_words = sorted(all_words.values(), key=lambda x: x['word'])

    with open('vocabularies/vocabulary.yaml', 'w') as f:
        yaml.dump(sorted_words, f, allow_unicode=True, sort_keys=False)

if __name__ == "__main__":
    consolidate_vocabularies()
    print("Consolidation complete. New file is vocabularies/vocabulary.yaml")
