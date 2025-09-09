import argparse
import os
import sys
from datetime import datetime
import yaml
import csv
import uuid

def generate_dialogue(date):
    """
    Generates a dialogue for the given date.

    For now, this returns a hardcoded dialogue.
    This could be replaced with a more sophisticated generation logic,
    such as a call to a language model.
    """
    base_title = "daily-standup-and-a-quick-sync"
    unique_id = uuid.uuid4().hex[:6]
    title = f"{base_title}-{unique_id}"
    dialogue_content = {
        "title": title,
        "dialogue": [
            {
                "speaker": "Maria",
                "english": "Morning, team! Quick stand-up. What's on everyone's plate today?",
                "bahasa": "Pagi, tim! Stand-up singkat. Apa yang ada di agenda kalian hari ini?"
            },
            {
                "speaker": "David",
                "english": "I'm still working on the caching layer for the user service. I think I can wrap it up by EOD.",
                "bahasa": "Aku masih mengerjakan lapisan caching untuk layanan pengguna. Sepertinya bisa kuselesaikan hari ini."
            },
            {
                "speaker": "Maria",
                "english": "Great. Any blockers?",
                "bahasa": "Bagus. Ada kendala?"
            },
            {
                "speaker": "David",
                "english": "Not at the moment. The documentation for the Redis library is pretty straightforward.",
                "bahasa": "Saat ini tidak ada. Dokumentasi untuk library Redis cukup jelas."
            },
            {
                "speaker": "Maria",
                "english": "Excellent. What about you, Chloe?",
                "bahasa": "Luar biasa. Bagaimana denganmu, Chloe?"
            },
            {
                "speaker": "Chloe",
                "english": "I'm going to start on the UI for the new reporting feature. I've got the mockups from the design team.",
                "bahasa": "Aku akan mulai mengerjakan UI untuk fitur pelaporan baru. Aku sudah dapat mockup dari tim desain."
            },
            {
                "speaker": "Maria",
                "english": "Perfect. After this, David, can we have a quick sync? I want to discuss the deployment strategy for your changes.",
                "bahasa": "Sempurna. Setelah ini, David, bisakah kita sinkronisasi sebentar? Aku ingin membahas strategi deployment untuk perubahanmu."
            },
            {
                "speaker": "David",
                "english": "Sure, ping me when you're ready.",
                "bahasa": "Tentu, hubungi aku jika sudah siap."
            }
        ],
        "expressions": [
            {
                "phrase": "What's on your plate?",
                "meaning_english": "What are you working on right now?",
                "meaning_bahasa": "Apa yang sedang kamu kerjakan saat ini?"
            },
            {
                "phrase": "Wrap it up by EOD",
                "meaning_english": "Finish it by the end of the day.",
                "meaning_bahasa": "Selesaikan pada akhir hari ini."
            },
            {
                "phrase": "Any blockers?",
                "meaning_english": "Are there any problems preventing you from making progress?",
                "meaning_bahasa": "Apakah ada masalah yang menghambat kemajuanmu?"
            },
            {
                "phrase": "A quick sync",
                "meaning_english": "A short meeting to make sure everyone is aligned.",
                "meaning_bahasa": "Rapat singkat untuk memastikan semua orang sepaham."
            },
            {
                "phrase": "Ping me",
                "meaning_english": "Contact me or send me a message.",
                "meaning_bahasa": "Hubungi aku atau kirimi aku pesan."
            }
        ],
        "questions": [
            {
                "q": "What is David's main task for the day?",
                "a": "David is working on implementing the caching layer for the user service."
            },
            {
                "q": "What will Chloe start working on?",
                "a": "Chloe will start working on the UI for the new reporting feature."
            },
            {
                "q": "Why does Maria want to sync with David?",
                "a": "Maria wants to discuss the deployment strategy for the changes David is making."
            }
        ]
    }
    return dialogue_content

def update_yaml_file(date, dialogue_data, dialogues_dir="dialogues"):
    """
    Creates or updates a YAML file for the given date.
    The file will contain a list of dialogues.
    """
    if not os.path.exists(dialogues_dir):
        os.makedirs(dialogues_dir)

    filepath = os.path.join(dialogues_dir, f"{date}.yaml")

    dialogues = []
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            try:
                dialogues = yaml.safe_load(f)
                if dialogues is None:
                    dialogues = []
            except yaml.YAMLError as e:
                print(f"Warning: Could not parse existing YAML file at {filepath}. Starting fresh. Error: {e}", file=sys.stderr)
                dialogues = []

    dialogues.append(dialogue_data)

    with open(filepath, 'w') as f:
        yaml.dump(dialogues, f, allow_unicode=True, sort_keys=False)

def update_csv_file(title, date, csv_filepath="dialogues.csv"):
    """
    Updates the CSV file with the new dialogue information.
    """
    file_exists = os.path.isfile(csv_filepath)
    with open(csv_filepath, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["title", "date"])
        writer.writerow([title, date])

def main():
    parser = argparse.ArgumentParser(description="Generate a daily English dialogue for a software developer.")
    parser.add_argument("date", help="The date for the dialogue in YYYY-MM-DD format.")
    args = parser.parse_args()

    try:
        # Validate the date format
        datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        print("Error: Date must be in YYYY-MM-DD format.", file=sys.stderr)
        sys.exit(1)

    dialogue_data = generate_dialogue(args.date)
    update_yaml_file(args.date, dialogue_data)
    update_csv_file(dialogue_data["title"], args.date)

    print(f"Successfully generated dialogue for {args.date}")

if __name__ == "__main__":
    main()
