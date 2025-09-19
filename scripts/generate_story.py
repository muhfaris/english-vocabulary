import argparse
import os
import sys
import datetime
import yaml
import csv
import random
import re

# Data Pools
# ---

STORY_TEMPLATES = [
    """
    Thursday morning started with my usual cup of coffee while I reviewed what was **{on_my_plate}** for the day. First up was the daily stand-up, where the team quickly synced on our progress. I had a couple of code reviews to get through, and a bug fix that needed immediate attention.

    My manager asked me to **{take_the_lead}** on a small feature enhancement. "Just **{reach_out}** to the design team to get the latest mockups," she said. "And please **{keep_me_posted}** on your progress."

    After the meeting, I decided to **{look_into}** the bug first. It was a bit tricky, but after about an hour of debugging, I found the root cause. I pushed the fix and after the CI/CD pipeline ran successfully, the feature was **{good_to_go}**.

    The rest of the afternoon was dedicated to the new feature. I wanted to **{stay_on_top_of}** it to make sure we could demo it by next week. I had a few questions for the backend team, so I sent them a message saying I'd **{get_back_to}** them with a more detailed query later. It was a productive day, and I felt a great sense of accomplishment.
    """
]

VOCABULARY_POOL = [
    {
        "word": "on my plate",
        "placeholder": "on_my_plate",
        "pronunciation": "/ɒn maɪ pleɪt/",
        "part_of_speech": "phrase",
        "meaning": {
            "english": "The tasks, responsibilities, or problems that one has to deal with.",
            "bahasa": "Tugas, tanggung jawab, atau masalah yang harus ditangani seseorang."
        },
        "usage": "Used to describe the work or responsibilities you currently have. It’s a common way to say you are busy or have a lot to do.",
        "synonyms": ["on my to-do list", "in my workload"],
        "examples": {
            "workplace": [
                "I can't take on another project right now; I have too much **on my plate**.",
                "Let's review what's **on your plate** for this sprint."
            ],
            "casual": [
                "With the new baby, I have a lot **on my plate** at home.",
                "She has enough **on her plate** without worrying about this."
            ]
        },
        "related": [
            {
                "word": "bandwidth",
                "difference": "'Bandwidth' refers to the capacity to take on new work, while 'on my plate' refers to the work you already have."
            },
            {
                "word": "workload",
                "difference": "'Workload' is a more formal term for the amount of work a person has. 'On my plate' is a more informal, idiomatic expression."
            }
        ],
        "story": "During the morning stand-up, I explained that I couldn't help with the new feature request this week because I already had too much **on my plate**. My manager understood and assigned the task to another developer."
    },
    {
        "word": "take the lead",
        "placeholder": "take_the_lead",
        "pronunciation": "/teɪk ðə liːd/",
        "part_of_speech": "phrase",
        "meaning": {
            "english": "To accept responsibility for a project or task and guide others.",
            "bahasa": "Menerima tanggung jawab atas suatu proyek atau tugas dan memandu orang lain."
        },
        "usage": "Used when someone is appointed or volunteers to be the main person responsible for a task, project, or initiative.",
        "synonyms": ["lead the way", "be in charge"],
        "examples": {
            "workplace": [
                "We need someone to **take the lead** on the database migration project.",
                "She decided to **take the lead** in organizing the team's offsite event."
            ],
            "casual": [
                "He decided to **take the lead** and plan the entire trip.",
                "Someone needs to **take the lead** in cleaning up this mess."
            ]
        },
        "related": [
            {
                "word": "delegate",
                "difference": "'Delegate' means to assign a task to someone else. 'Take the lead' means to become the leader of a task yourself."
            },
            {
                "word": "manage",
                "difference": "'Manage' is a broader term for overseeing projects or people. 'Take the lead' is more specific to starting a new initiative or taking responsibility for a particular task."
            }
        ],
        "story": "Our team was struggling to decide on a new frontend framework. After a long discussion, Sarah decided to **take the lead**. She created a comparison document and scheduled a meeting to present her findings, which helped us make a final decision."
    },
    {
        "word": "reach out",
        "placeholder": "reach_out",
        "pronunciation": "/riːtʃ aʊt/",
        "part_of_speech": "phrase",
        "meaning": {
            "english": "To try to communicate with a person or a group of people.",
            "bahasa": "Mencoba untuk berkomunikasi dengan seseorang atau sekelompok orang."
        },
        "usage": "A common and slightly more formal way to say 'contact' or 'get in touch with'. It's often used in a professional context.",
        "synonyms": ["contact", "get in touch"],
        "examples": {
            "workplace": [
                "Please **reach out** to the support team if you encounter any issues.",
                "I'll **reach out** to the client to get more details on their requirements."
            ],
            "casual": [
                "Don't hesitate to **reach out** if you need anything.",
                "He decided to **reach out** to an old friend he hadn't spoken to in years."
            ]
        },
        "related": [
            {
                "word": "ping",
                "difference": "'Ping' is a very informal, quick way to contact someone, often online (e.g., 'ping me on Slack'). 'Reach out' is more general and can be used for emails, calls, or other forms of communication."
            },
            {
                "word": "contact",
                "difference": "'Contact' is a neutral, standard term. 'Reach out' often implies an attempt to establish a connection or offer help, making it sound a bit warmer."
            }
        ],
        "story": "I was stuck on a complex bug, so I decided to **reach out** to a senior developer on another team who had experience with that part of the codebase. She was very helpful and pointed me in the right direction."
    },
    {
        "word": "keep me posted",
        "placeholder": "keep_me_posted",
        "pronunciation": "/kiːp miː ˈpoʊstɪd/",
        "part_of_speech": "phrase",
        "meaning": {
            "english": "To keep someone informed of the latest developments or news about a situation.",
            "bahasa": "Untuk memberi tahu seseorang tentang perkembangan atau berita terbaru tentang suatu situasi."
        },
        "usage": "An informal way to ask for regular updates on a task, project, or situation. It’s friendly and common in workplace communication.",
        "synonyms": ["keep me updated", "keep me in the loop"],
        "examples": {
            "workplace": [
                "**Keep me posted** on the status of the server deployment.",
                "I'm waiting for the client's feedback, so please **keep me posted**."
            ],
            "casual": [
                "I hope you feel better soon! **Keep me posted**.",
                "Let me know how the job interview goes. **Keep me posted**!"
            ]
        },
        "related": [
            {
                "word": "update me",
                "difference": "'Update me' is a direct request for information. 'Keep me posted' is a slightly more informal and ongoing request for updates over time."
            },
            {
                "word": "notify me",
                "difference": "'Notify me' is more formal and often used for official communications or automated alerts (e.g., 'notify me when the build is complete'). 'Keep me posted' is for personal, informal communication."
            }
        ],
        "story": "Before leaving for the day, my manager said, \"I know you're working on that critical bug fix. **Keep me posted** on your progress tomorrow morning.\" This way, she knows I'll give her an update as soon as I have one."
    },
    {
        "word": "look into",
        "placeholder": "look_into",
        "pronunciation": "/lʊk ˈɪntuː/",
        "part_of_speech": "phrase",
        "meaning": {
            "english": "To investigate or examine something.",
            "bahasa": "Menyelidiki atau memeriksa sesuatu."
        },
        "usage": "A common way to say you are going to investigate a problem, question, or issue. It implies a process of examination.",
        "synonyms": ["investigate", "check out"],
        "examples": {
            "workplace": [
                "A customer reported an issue with logging in. Can you **look into** it?",
                "I'm not sure what's causing the error, but I'll **look into** it right away."
            ],
            "casual": [
                "My internet is slow. I need to **look into** why.",
                "Thanks for the suggestion. I'll **look into** that restaurant."
            ]
        },
        "related": [
            {
                "word": "investigate",
                "difference": "'Investigate' is more formal and often implies a more thorough, systematic examination. 'Look into' is more common in everyday conversation."
            },
            {
                "word": "debug",
                "difference": "'Debug' is specific to finding and fixing errors in code. 'Look into' is a more general term for examining any kind of problem or question."
            }
        ],
        "story": "During the demo, we noticed that the new feature was running slower than expected. My team lead asked me to **look into** it and see if I could identify any performance bottlenecks in the code."
    },
    {
        "word": "good to go",
        "placeholder": "good_to_go",
        "pronunciation": "/ɡʊd tuː ɡoʊ/",
        "part_of_speech": "phrase",
        "meaning": {
            "english": "Ready, prepared, or approved to proceed.",
            "bahasa": "Siap, siap, atau disetujui untuk melanjutkan."
        },
        "usage": "An informal, friendly phrase used to confirm that something is ready or someone is prepared to start.",
        "synonyms": ["all set", "ready to roll"],
        "examples": {
            "workplace": [
                "The tests have all passed, so the new feature is **good to go** for deployment.",
                "I've finished the report. It's **good to go**."
            ],
            "casual": [
                "I've packed my bags. I'm **good to go** for the trip.",
                "Is the coffee ready? Yes, it's **good to go**."
            ]
        },
        "related": [
            {
                "word": "ready",
                "difference": "'Ready' is a standard, neutral term. 'Good to go' is more informal and often adds a sense of positive confirmation or enthusiasm."
            },
            {
                "word": "approved",
                "difference": "'Approved' is a formal term indicating official permission. 'Good to go' is an informal way to say something has been checked and is ready, which might imply approval but doesn't state it formally."
            }
        ],
        "story": "After I pushed my latest changes, the CI/CD pipeline automatically ran all the tests. A few minutes later, I got a green checkmark. Everything passed, so my code was **good to go** for merging into the main branch."
    },
    {
        "word": "stay on top of",
        "placeholder": "stay_on_top_of",
        "pronunciation": "/steɪ ɒn tɒp ʌv/",
        "part_of_speech": "phrase",
        "meaning": {
            "english": "To remain in control or fully informed about something, especially when it's changing quickly.",
            "bahasa": "Untuk tetap memegang kendali atau mendapat informasi lengkap tentang sesuatu, terutama ketika itu berubah dengan cepat."
        },
        "usage": "Used to describe the act of managing your tasks, information, or responsibilities proactively so that you don't fall behind.",
        "synonyms": ["keep up with", "manage effectively"],
        "examples": {
            "workplace": [
                "With so many emails, it's hard to **stay on top of** everything.",
                "As a project manager, her job is to **stay on top of** all the moving parts."
            ],
            "casual": [
                "I read the news every day to **stay on top of** current events.",
                "It's important to **stay on top of** your finances."
            ]
        },
        "related": [
            {
                "word": "manage",
                "difference": "'Manage' is a general term for handling something. 'Stay on top of' specifically implies dealing with something that requires continuous attention to avoid problems."
            },
            {
                "word": "follow",
                "difference": "'Follow' can mean to track something, but 'stay on top of' implies a more active role in controlling or managing it."
            }
        ],
        "story": "The project had a very tight deadline, so I created a detailed task list to help me **stay on top of** all my responsibilities. Checking off items each day helped me ensure nothing was forgotten."
    },
    {
        "word": "get back to",
        "placeholder": "get_back_to",
        "pronunciation": "/ɡɛt bæk tuː/",
        "part_of_speech": "phrase",
        "meaning": {
            "english": "To contact someone again later to give them information or a response.",
            "bahasa": "Menghubungi seseorang lagi nanti untuk memberi mereka informasi atau tanggapan."
        },
        "usage": "A common phrase used when you can't answer a question or provide information immediately and promise to do so later.",
        "synonyms": ["follow up with", "respond to later"],
        "examples": {
            "workplace": [
                "I don't have the answer right now, but I'll find out and **get back to** you.",
                "She said she would check the data and **get back to** me by the end of the day."
            ],
            "casual": [
                "Can I **get back to** you on that? I need to check my calendar.",
                "He'll **get back to** you about the party plans."
            ]
        },
        "related": [
            {
                "word": "respond",
                "difference": "'Respond' is a general term for answering. 'Get back to' specifically implies a delay between the question and the answer."
            },
            {
                "word": "reply",
                "difference": "'Reply' is often used for written communication (e.g., 'reply to an email'). 'Get back to' can be used for any form of communication (call, message, in person)."
            }
        ],
        "story": "A colleague asked me a question about an old project, but I couldn't remember the details. I told them, \"I need to check my notes, but I will **get back to** you before the end of the day.\""
    }
]


# Core Functions
# ---

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

def select_new_vocabulary(existing_vocab):
    """Selects new vocabulary words that are not in the existing set."""
    new_words_pool = [
        v for v in VOCABULARY_POOL
        if v['word'].lower() not in existing_vocab
    ]

    # For this script, we assume the template requires all words in the pool
    required_placeholders = {
        re.sub(r'[{}]', '', p) for p in re.findall(r'{\w+}', STORY_TEMPLATES[0])
    }

    selected_vocab = [
        v for v in new_words_pool if v.get('placeholder') in required_placeholders
    ]

    if len(selected_vocab) < len(required_placeholders):
        print(f"Error: Not enough new words in the pool to fill the template.", file=sys.stderr)
        print(f"Required: {len(required_placeholders)}, Found: {len(selected_vocab)}", file=sys.stderr)
        sys.exit(1)

    return selected_vocab

def generate_kebab_case_title(text, num_words=4):
    """Generates a kebab-case title from the first few words of a text."""
    text = text.replace('**', '')
    words = re.findall(r'\b\w+\b', text.lower())
    return '-'.join(words[:num_words])

def generate_story_content(new_vocab_list):
    """Generates the story text, title, and highlighted words list."""
    template = random.choice(STORY_TEMPLATES)

    vocab_map = {v['placeholder']: v['word'] for v in new_vocab_list}

    story_text = template.format(**vocab_map).strip()

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

    existing_vocab = []
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                existing_vocab = yaml.safe_load(f) or []
                if not isinstance(existing_vocab, list):
                    print(f"Warning: Existing vocabulary file {filepath} is not a list. Overwriting.", file=sys.stderr)
                    existing_vocab = []
            except yaml.YAMLError as e:
                print(f"Warning: Could not parse {filepath}. Overwriting. Error: {e}", file=sys.stderr)
                existing_vocab = []

    existing_words_in_file = {v['word'] for v in existing_vocab}
    for new_vocab in new_vocab_list:
        if new_vocab['word'] not in existing_words_in_file:
            # Remove placeholder before saving
            vocab_to_save = new_vocab.copy()
            vocab_to_save.pop('placeholder', None)
            existing_vocab.append(vocab_to_save)

    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump(existing_vocab, f, allow_unicode=True, sort_keys=False, indent=2)
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

    existing_vocab = load_existing_vocab()
    print(f"Loaded {len(existing_vocab)} existing vocabulary words.")

    new_vocab_list = select_new_vocabulary(existing_vocab)
    print(f"Selected {len(new_vocab_list)} new words: {[v['word'] for v in new_vocab_list]}")

    story_content = generate_story_content(new_vocab_list)
    story_content['date'] = args.date
    print(f"Generated story with title: '{story_content['title']}'")

    # Before creating new files, let's remove the old one if it exists to avoid confusion
    old_story_file = 'stories/story-thursday-morning-started-with.yaml'
    if os.path.exists(old_story_file):
        os.remove(old_story_file)

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
