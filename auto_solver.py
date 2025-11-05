#!/usr/bin/env python3
"""
Auto-solver for daily LeetCode problems using OpenAI GPT-5-mini.
This script fetches the daily problem, uses AI to solve it, and creates a solution file.
"""

import os
import sys
import json
import requests
from datetime import datetime
from openai import OpenAI


def fetch_daily_problem():
    """
    Fetch the daily LeetCode problem details using the GraphQL API.
    
    Returns:
        dict: Problem details including ID, title, description, etc.
    """
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
                    content
                    exampleTestcases
                }
            }
        }""",
        "operationName": "questionOfToday"
    }
    
    try:
        response = requests.post(leetcode_api_url, json=daily_challenge_query)
        response.raise_for_status()
        data = response.json()
        
        if 'data' in data and 'activeDailyCodingChallengeQuestion' in data['data']:
            problem_data = data['data']['activeDailyCodingChallengeQuestion']
            question = problem_data['question']
            
            return {
                'problem_id': question['questionFrontendId'],
                'title': question['title'],
                'title_slug': question['titleSlug'],
                'difficulty': question['difficulty'],
                'content': question['content'],
                'link': f"https://leetcode.com/problems/{question['titleSlug']}/description/?envType=daily-question",
                'example_testcases': question.get('exampleTestcases', '')
            }
        else:
            print("Error: Unexpected response structure from LeetCode API")
            print(json.dumps(data, indent=2))
            return None
            
    except Exception as e:
        print(f"Error fetching daily problem: {e}")
        return None


def generate_solution_with_ai(problem_info, api_key):
    """
    Use OpenAI GPT-5-mini to generate a solution for the problem.
    
    Args:
        problem_info (dict): Problem details from LeetCode
        api_key (str): OpenAI API key
        
    Returns:
        str: Generated solution in markdown format
    """
    try:
        client = OpenAI(api_key=api_key)
        
        # Create a detailed prompt for the AI
        prompt = f"""You are solving a LeetCode problem. Generate a complete solution following this exact format:

# [Problem {problem_info['problem_id']}: {problem_info['title']}]({problem_info['link']})

## Initial thoughts (stream-of-consciousness)
[Provide your initial thoughts about the problem, what approach comes to mind first, any observations about the problem structure]

## Refining the problem, round 2 thoughts
[Discuss any refinements to your approach, edge cases to consider, alternative solutions, time/space complexity considerations]

## Attempted solution(s)
```python
[Provide a complete, working Python solution]
```
- [Add brief notes about the solution approach, complexity analysis, and any important implementation details]

Here is the problem:

**Title:** {problem_info['title']}
**Difficulty:** {problem_info['difficulty']}
**Link:** {problem_info['link']}

**Problem Description:**
{problem_info['content']}

Please provide a thoughtful, well-explained solution that demonstrates clear problem-solving skills. The solution should be efficient and include proper complexity analysis."""

        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role": "system", "content": "You are an expert software engineer solving LeetCode problems. Provide clear explanations and efficient solutions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error generating solution with AI: {e}")
        return None


def save_solution(problem_id, solution_content):
    """
    Save the generated solution to the appropriate file.
    
    Args:
        problem_id (str): The LeetCode problem ID
        solution_content (str): The markdown content to save
        
    Returns:
        str: Path to the created file
    """
    try:
        problem_dir = f"problems/{problem_id}"
        os.makedirs(problem_dir, exist_ok=True)
        
        solution_file = f"{problem_dir}/gpt5-mini.md"
        
        with open(solution_file, 'w', encoding='utf-8') as f:
            f.write(solution_content)
        
        print(f"Solution saved to: {solution_file}")
        return solution_file
        
    except Exception as e:
        print(f"Error saving solution: {e}")
        return None


def main():
    """Main execution function."""
    print("=" * 60)
    print("LeetCode Auto-Solver - Starting...")
    print("=" * 60)
    
    # Get OpenAI API key from environment
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        sys.exit(1)
    
    # Fetch today's problem
    print("\n1. Fetching daily LeetCode problem...")
    problem_info = fetch_daily_problem()
    if not problem_info:
        print("Failed to fetch daily problem")
        sys.exit(1)
    
    print(f"   Problem ID: {problem_info['problem_id']}")
    print(f"   Title: {problem_info['title']}")
    print(f"   Difficulty: {problem_info['difficulty']}")
    
    # Generate solution using AI
    print("\n2. Generating solution with GPT-5-mini...")
    solution = generate_solution_with_ai(problem_info, api_key)
    if not solution:
        print("Failed to generate solution")
        sys.exit(1)
    
    print("   Solution generated successfully!")
    
    # Save the solution
    print("\n3. Saving solution to file...")
    saved_path = save_solution(problem_info['problem_id'], solution)
    if not saved_path:
        print("Failed to save solution")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("Auto-solver completed successfully!")
    print("=" * 60)
    

if __name__ == "__main__":
    main()
