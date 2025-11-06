import requests
import json
from datetime import datetime
import re
from collections import defaultdict

# Set variables
date_str = datetime.now().strftime('%B %-d, %Y')
repo_url = "https://github.com/ContextLab/leetcode-solutions"
readme_file = "README.md"
leetcode_api_url = "https://leetcode.com/graphql"
daily_challenge_query = {
    "query": """query questionOfToday {
        activeDailyCodingChallengeQuestion {
            date
            link
            question {
                questionFrontendId
                title
                titleSlug
                difficulty
            }
        }
    }""",
    "operationName": "questionOfToday"
}

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

def generate_collapsible_sections(entries_by_month, current_month_key):
    """Generate HTML collapsible sections for each month."""
    sections = []

    # Sort months in descending order (most recent first)
    sorted_months = sorted(entries_by_month.keys(), reverse=True)

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

# Fetch daily challenge details from API
response = requests.post(leetcode_api_url, json=daily_challenge_query)
data = response.json()

# Debug: Print the entire response to check its structure
print(json.dumps(data, indent=2))

# Check if the expected data is present in the API response
if 'data' in data and 'activeDailyCodingChallengeQuestion' in data['data']:
    problem = data['data']['activeDailyCodingChallengeQuestion']['question']
    problem_id = problem['questionFrontendId']
    title = problem['title']
    title_slug = problem['titleSlug']
    link = f"https://leetcode.com/problems/{title_slug}/description/?envType=daily-question"
    difficulty = problem['difficulty']
    difficulty_icon = "🟢" if difficulty == "Easy" else "🟡" if difficulty == "Medium" else "🔴"
    note_link = f"{repo_url}/tree/main/problems/{problem_id}"

    # Print the fetched problem details for debugging
    print(f"Problem ID: {problem_id}")
    print(f"Title: {title}")
    print(f"Title Slug: {title_slug}")
    print(f"Link: {link}")
    print(f"Difficulty: {difficulty}")

    # Create the new entry
    new_entry = f"| {date_str} | [{problem_id}]({link}) | [Click here]({note_link}) | {difficulty_icon} {difficulty} |"

    # Parse current date to get month key
    current_dt, current_month_key = parse_date(date_str)

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

    # Add the new entry to the appropriate month
    if current_month_key:
        entries_by_month[current_month_key].append(new_entry)

    # Generate collapsible sections
    formatted_table = generate_collapsible_sections(entries_by_month, current_month_key)

    # Rebuild the README with collapsible sections
    updated_readme = ''.join(before_table) + '\n' + formatted_table + '\n' + ''.join(after_table)

    # Overwrite the README file with the updated content
    with open(readme_file, 'w') as file:
        file.write(updated_readme)

    print("README file updated successfully with collapsible month sections!")
else:
    print("Error: Unexpected response structure.")
