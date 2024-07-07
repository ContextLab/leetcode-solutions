import requests
import json
from datetime import datetime

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
    updated_readme = before_table + table_content + [new_entry + '\n\n'] + after_table

    # Overwrite the README file with the updated content
    with open(readme_file, 'w') as file:
        file.writelines(updated_readme)

    print("README file updated successfully!")
else:
    print("Error: Unexpected response structure.")
