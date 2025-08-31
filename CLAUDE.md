# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an English vocabulary learning platform specifically designed for software engineers to master professional workplace communication. It provides interactive flash cards with vocabulary commonly used in meetings, code reviews, and daily work conversations.

## Data Structure & Architecture

### Core Components

The project is structured around YAML data files organized in three main categories:

1. **Vocabularies** (`/vocabularies/`) - Daily vocabulary entries with detailed definitions
   - Format: `vocabulary - YYYY-MM-DD.yaml` or `vocabulary from story - YYYY-MM-DD.yaml`
   - Each entry contains: word, pronunciation, part of speech, meaning (English/Bahasa), usage guidelines, synonyms, workplace/casual examples, related words, and contextual stories

2. **Stories** (`/stories/`) - Narrative content featuring highlighted vocabulary
   - Format: `story-[title].yaml`
   - Structure: title, date, text with **highlighted_words**, and list of highlighted terms

3. **Dialogues** (`/dialogues/`) - Conversational examples showing vocabulary usage
   - Bilingual dialogue format with English and Bahasa Indonesia translations

### Data Quality

- Use `python scripts/check_duplicates.py` to verify no duplicate vocabulary words or story titles exist
- All vocabulary entries must include comprehensive examples for both workplace and casual contexts
- Stories should naturally incorporate vocabulary terms with contextual usage

## Common Development Tasks

### Data Validation
```bash
python scripts/check_duplicates.py
```
This script checks for duplicate vocabulary words across all vocabulary files and duplicate story titles across all story files. Returns exit code 1 if duplicates are found.

### Content Guidelines

**Vocabulary Entries:**
- Include pronunciation using IPA notation
- Provide both English and Bahasa Indonesia meanings
- Add workplace-specific usage examples
- Include related words with clear distinctions
- Write contextual stories showing natural usage

**Stories:**
- Use bold formatting (`**word**`) for highlighted vocabulary
- Keep stories relatable to software engineering contexts
- Ensure highlighted words have corresponding vocabulary entries

**File Naming:**
- Vocabularies: `vocabulary - YYYY-MM-DD.yaml`
- Stories: `story-[descriptive-title].yaml`
- Dialogues: `[descriptive-name].yaml`

This is a content-focused repository with no build process, dependencies, or traditional development setup required.