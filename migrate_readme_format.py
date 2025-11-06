#!/usr/bin/env python3
"""
One-time migration script to convert the README table to collapsible month sections.
"""

import re
from datetime import datetime
from collections import defaultdict

readme_file = "README.md"

def parse_date(date_str):
    """Parse date string and return datetime object and (year, month) tuple."""
    try:
        dt = datetime.strptime(date_str, '%B %d, %Y')
        return dt, (dt.year, dt.month)
    except:
        return None, None

def format_month_year(year, month):
    """Format month and year as 'Month, Year'."""
    return datetime(year, month, 1).strftime('%B, %Y')

def parse_table_entries(lines):
    """Parse existing table entries and group them by month."""
    entries_by_month = defaultdict(list)
    table_pattern = re.compile(r'^\| (.+?) \| (.+?) \| (.+?) \| (.+?) \|')

    for line in lines:
        line = line.strip()
        if not line or line.startswith('|---') or line.startswith('| 📆'):
            continue

        match = table_pattern.match(line)
        if match:
            date_str = match.group(1).strip()
            dt, month_key = parse_date(date_str)
            if month_key:
                entries_by_month[month_key].append(line)

    return entries_by_month

def generate_collapsible_sections(entries_by_month):
    """Generate HTML collapsible sections for each month."""
    sections = []

    # Sort months in descending order (most recent first)
    sorted_months = sorted(entries_by_month.keys(), reverse=True)

    # Get the most recent month to keep it open
    current_month_key = sorted_months[0] if sorted_months else None

    table_header = """| 📆 Date         | ⚙️ Problem                                                                                                     | 📝 Link to notes                                                                                             | 🚦 Difficulty |
|--------------|-------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|------------|"""

    for month_key in sorted_months:
        year, month = month_key
        month_name = format_month_year(year, month)
        entries = entries_by_month[month_key]

        # Only the current month should be open
        open_attr = ' open' if month_key == current_month_key else ''

        sections.append(f'<details{open_attr}>')
        sections.append(f'<summary><b>Problems from {month_name}</b></summary>')
        sections.append('')
        sections.append(table_header)

        for entry in entries:
            sections.append(entry)

        sections.append('')
        sections.append('</details>')
        sections.append('')

    return '\n'.join(sections)

# Read the entire README file
with open(readme_file, 'r') as file:
    lines = file.readlines()

# Initialize variables to store parts of the README
before_table = []
table_content = []
after_table = []
in_table_section = False

# Process the README line by line
for line in lines:
    if "Problems we've attempted so far:" in line:
        in_table_section = True
        before_table.append(line)
    elif "# Join our discussion!" in line:
        in_table_section = False
        after_table.append(line)
    elif in_table_section:
        table_content.append(line)
    else:
        if table_content:
            after_table.append(line)
        else:
            before_table.append(line)

# Parse existing table entries
entries_by_month = parse_table_entries(table_content)

print(f"Found {len(entries_by_month)} months of data")
for month_key in sorted(entries_by_month.keys(), reverse=True):
    year, month = month_key
    print(f"  {format_month_year(year, month)}: {len(entries_by_month[month_key])} problems")

# Generate collapsible sections
formatted_table = generate_collapsible_sections(entries_by_month)

# Rebuild the README with collapsible sections
updated_readme = ''.join(before_table) + '\n' + formatted_table + '\n' + ''.join(after_table)

# Overwrite the README file with the updated content
with open(readme_file, 'w') as file:
    file.write(updated_readme)

print("\nREADME file successfully migrated to collapsible month sections!")
