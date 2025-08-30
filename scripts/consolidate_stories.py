import os
import yaml

def consolidate_stories():
    all_stories = {}
    for filename in os.listdir('stories'):
        if filename.endswith('.yaml'):
            with open(os.path.join('stories', filename), 'r') as f:
                data = yaml.safe_load(f)
                if data and 'story' in data and 'title' in data['story']:
                    title = data['story']['title']
                    if title not in all_stories:
                        all_stories[title] = data

    # Sort by title for consistency
    sorted_stories = sorted(all_stories.values(), key=lambda x: x['story']['title'])

    with open('stories/stories.yaml', 'w') as f:
        yaml.dump(sorted_stories, f, allow_unicode=True, sort_keys=False)

if __name__ == "__main__":
    consolidate_stories()
    print("Consolidation complete. New file is stories/stories.yaml")
