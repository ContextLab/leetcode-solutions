import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup

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

# Fetch daily challenge details from API
response = requests.post(leetcode_api_url, json=daily_challenge_query)
data = response.json()

# Debug: Print the entire response to check its structure
print(json.dumps(data, indent=2))

# Fetch the daily challenge details from the daily challenge page for verification
daily_challenge_page = requests.get("https://leetcode.com/problemset/all/")
soup = BeautifulSoup(daily_challenge_page.content, 'html.parser')

# Initialize variables for cross-verified details
daily_challenge_title = None
daily_challenge_slug = None
daily_challenge_id = None

# Attempt to fetch the daily challenge details
try:
    daily_challenge_section = soup.find('div', {'class': 'question-list-table'})
    if daily_challenge_section:
        first_problem = daily_challenge_section.find_all('tr')[1]  # Skip header row
        daily_challenge_title = first_problem.find('a', {'class': 'title'}).text.strip()
        daily_challenge_slug = first_problem.find('a', {'class': 'title'})['href'].strip().split('/')[-2]
        daily_challenge_id = first_problem.find_all('td')[1].text.strip()

        # Print the cross-verified details for debugging
        print(f"Cross-verified Title: {daily_challenge_title}")
        print(f"Cross-verified Slug: {daily_challenge_slug}")
        print(f"Cross-verified ID: {daily_challenge_id}")
    else:
        raise Exception("Error: Could not fetch the daily challenge from the problem set page.")
except Exception as e:
    print(f"Error: Exception occurred while fetching daily challenge details: {e}")
    raise

# Check if the expected data is present in the API response
if 'data' in data and 'activeDailyCodingChallengeQuestion' in data['data']:
    problem = data['data']['activeDailyCodingChallengeQuestion']['question']
    problem_id = problem['questionId']
    title = problem['title']
    title_slug = problem['titleSlug']
    link = f"https://leetcode.com/problems/{title_slug}"
    difficulty = problem['difficulty']
    difficulty_icon = "🟢" if difficulty == "Easy" else "🟡" if difficulty == "Medium" else "🔴"
    note_link = f"{repo_url}/tree/main/problems/{problem_id}"

    # Print the API details for debugging
    print(f"API Title: {title}")
    print(f"API Slug: {title_slug}")
    print(f"API ID: {problem_id}")

    # Check if the API title and slug match the cross-verified title and slug
    if daily_challenge_title and (daily_challenge_title != title or daily_challenge_slug != title_slug):
        raise Exception("Error: The titles or slugs do not match. The API might be providing incorrect details.")

    # Create the new entry
    new_entry = f"| {date_str} | [{problem_id}]({link}) | [Click here]({note_link}) | {difficulty_icon} {difficulty} |"

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

    # Strip trailing whitespace from the last row of the table content
    if table_content:
        table_content[-1] = table_content[-1].rstrip()

    # Rebuild the README with the new entry added to the table
    updated_readme = before_table + table_content + [new_entry + '\n'] + after_table

    # Overwrite the README file with the updated content
    with open(readme_file, 'w') as file:
        file.writelines(updated_readme)

    print("README file updated successfully!")
else:
    raise Exception("Error: Unexpected response structure.")
