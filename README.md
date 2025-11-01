# Games Dataset Cleaning Script

This repository contains a Python script for cleaning and processing a games dataset CSV file.

## What This Script Does

The `clean_games.py` script performs the following data cleaning operations:

1. **Removes redundant index column** - Eliminates the unnecessary first column containing row numbers
2. **Removes Summary column** - Drops the text-heavy summary field to reduce file size
3. **Removes exact duplicates** - Eliminates duplicate rows (382 duplicates removed)
4. **Converts release dates to years** - Changes "Feb 25, 2022" to "2022"
5. **Converts list fields to semicolon-separated values**:
   - Team: `['Bandai Namco', 'FromSoftware']` → `Bandai Namco; FromSoftware`
   - Genres: `['Adventure', 'RPG']` → `Adventure; RPG`
6. **Converts numeric notation to actual numbers**:
   - `3.9K` → `3900`
   - `2.5M` → `2500000`

## Dataset Information

- **Original file size**: 2.7MB with 1,512 rows
- **Cleaned file size**: 1.5MB with 1,130 unique rows
- **Columns**: Title, Release Date, Team, Rating, Times Listed, Number of Reviews, Genres, Reviews, Plays, Playing, Backlogs, Wishlist

## Usage

```bash
python3 clean_games.py
```

The script reads from `games.csv` and outputs to `games_cleaned.csv`.

## Requirements

- Python 3.x
- Standard library modules: `csv`, `ast`, `datetime`

## Output

The cleaned CSV file will have:
- No redundant columns
- No duplicate entries
- Standardized date formats (years only)
- Semicolon-separated list values
- Numeric values instead of K/M notation
