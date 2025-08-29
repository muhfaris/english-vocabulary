# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This is an English Vocabulary Learning Application with a static HTML site that loads vocabulary data from YAML files. The application is containerized using Docker and serves a vocabulary learning interface with search, filtering, and detailed word modals.

## Architecture
- **Static Site**: Single-page HTML application located in `/site/index.html`
- **Vocabulary Data**: YAML files in `/vocabularies/` directory with naming pattern `vocabulary - YYYY-MM-DD.yaml`
- **Deployment**: Docker container using nginx to serve static files

## Vocabulary Data Structure
Each YAML file contains an array of vocabulary objects with this structure:
- `word`: The vocabulary word
- `meaning`: Object with `english` and `bahasa` (Indonesian) translations
- `usage`: Usage guide string
- `examples`: Object with `workplace` and `casual` arrays of example sentences
- `related`: Array of related words with `word` and `difference` fields
- `story`: Context story string (optional)

## Commands
- **Build container**: `docker build -t english-vocabulary .`
- **Run container**: `docker run -p 8080:80 english-vocabulary`
- **Development**: Open `/site/index.html` directly in browser for local development

## Key Features
- Dynamic vocabulary loading from GitHub repository
- Date-based filtering for vocabulary sets
- Search across all vocabulary fields
- Detailed modal view with examples and context
- Mobile-responsive design
- Progress tracking (learned words counter)

## Technical Notes
- Uses `js-yaml` library via CDN for YAML parsing
- Fetches vocabulary from GitHub raw content URLs
- No build system - pure HTML/CSS/JavaScript
- Responsive grid layout for vocabulary cards
- Modal system for detailed word information