import json
import os

# Load problem details
with open("problem_details.json", "r") as f:
    problem_details = json.load(f)

# Define paths
template_path = "problems/template.md"
problem_dir = f"problems/{problem_details['questionId']}"
github_username = os.getenv('GITHUB_USERNAME')
problem_file = f"{problem_dir}/{github_username}.md"  # Replace with actual username

# Create problem directory if it doesn't exist
os.makedirs(problem_dir, exist_ok=True)

# Read template content
with open(template_path, "r") as f:
    template_content = f.read()

# Customize template with problem details
note_content = template_content.replace("<NUMBER>", problem_details['questionId'])
note_content = note_content.replace("<TITLE>", problem_details['title'])
note_content = note_content.replace("<LINK TO DESCRIPTION>", problem_details['link'])

# Write customized note to new file
with open(problem_file, "w") as f:
    f.write(note_content)
