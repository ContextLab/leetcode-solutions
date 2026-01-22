#!/usr/bin/env python3
"""
Bulk solver for adding AI-generated solutions to missing LeetCode problems.
This script fetches problem details from LeetCode and generates solutions using GPT-5-mini.
"""

import os
import sys
import json
import time
import requests
from openai import OpenAI
from pathlib import Path


def fetch_problem_by_id(problem_id):
    """
    Fetch a specific LeetCode problem by its ID using the GraphQL API.
    
    Args:
        problem_id (str): The problem ID (e.g., "1", "2", "100")
    
    Returns:
        dict: Problem details or None if not found
    """
    leetcode_api_url = "https://leetcode.com/graphql"
    
    # First, we need to get the titleSlug for the problem
    # We'll use a query that searches for problems
    query = {
        "query": """query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
            problemsetQuestionList: questionList(
                categorySlug: $categorySlug
                limit: $limit
                skip: $skip
                filters: $filters
            ) {
                questions: data {
                    questionFrontendId
                    title
                    titleSlug
                    difficulty
                    content
                }
            }
        }""",
        "variables": {
            "categorySlug": "algorithms",
            "skip": 0,
            "limit": 5000,
            "filters": {}
        },
        "operationName": "problemsetQuestionList"
    }
    
    try:
        response = requests.post(leetcode_api_url, json=query, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if 'data' in data and 'problemsetQuestionList' in data['data']:
            questions = data['data']['problemsetQuestionList']['questions']
            
            # Find the problem with matching ID
            for question in questions:
                if question['questionFrontendId'] == str(problem_id):
                    # Now fetch full details including content
                    return fetch_problem_details(question['titleSlug'])
            
            print(f"Problem {problem_id} not found in LeetCode database")
            return None
        else:
            print(f"Unexpected response structure for problem {problem_id}")
            return None
            
    except Exception as e:
        print(f"Error fetching problem {problem_id}: {e}")
        return None


def fetch_problem_details(title_slug):
    """
    Fetch detailed problem information including content.
    
    Args:
        title_slug (str): The problem's title slug
    
    Returns:
        dict: Problem details
    """
    leetcode_api_url = "https://leetcode.com/graphql"
    query = {
        "query": """query questionData($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionFrontendId
                title
                titleSlug
                difficulty
                content
            }
        }""",
        "variables": {"titleSlug": title_slug},
        "operationName": "questionData"
    }
    
    try:
        response = requests.post(leetcode_api_url, json=query, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if 'data' in data and 'question' in data['data']:
            question = data['data']['question']
            return {
                'problem_id': question['questionFrontendId'],
                'title': question['title'],
                'title_slug': question['titleSlug'],
                'difficulty': question['difficulty'],
                'content': question['content'],
                'link': f"https://leetcode.com/problems/{question['titleSlug']}/description/?envType=daily-question"
            }
        else:
            print(f"Error: Could not fetch details for {title_slug}")
            return None
            
    except Exception as e:
        print(f"Error fetching problem details for {title_slug}: {e}")
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
        import httpx

        # Create an httpx client that doesn't verify SSL certificates
        http_client = httpx.Client(verify=False)
        client = OpenAI(api_key=api_key, http_client=http_client)

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
            max_completion_tokens=8000
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
        
        print(f"  ✓ Solution saved to: {solution_file}")
        return solution_file
        
    except Exception as e:
        print(f"  ✗ Error saving solution: {e}")
        return None


def get_existing_problems():
    """Get a set of problem IDs that already have solutions."""
    problems_dir = Path("problems")
    if not problems_dir.exists():
        return set()
    
    existing = set()
    for item in problems_dir.iterdir():
        if item.is_dir() and item.name.isdigit():
            existing.add(int(item.name))
    
    return existing


def main():
    """Main execution function."""
    print("=" * 70)
    print("LeetCode Bulk Solver - Adding AI-generated solutions for missing problems")
    print("=" * 70)
    
    # Check for dry-run mode
    dry_run = '--dry-run' in sys.argv
    if dry_run:
        sys.argv.remove('--dry-run')
        print("\n*** DRY RUN MODE - Will not generate solutions ***\n")
    
    # Get OpenAI API key from environment
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key and not dry_run:
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Use --dry-run flag to test without API key")
        sys.exit(1)
    
    # Get list of problems to solve
    if len(sys.argv) >= 2:
        # Read from file
        problems_file = sys.argv[1]
        print(f"\nReading problems from: {problems_file}")
        
        with open(problems_file, 'r') as f:
            problems_to_solve = [int(line.strip()) for line in f if line.strip()]
        
        print(f"Found {len(problems_to_solve)} problems to solve")
    else:
        print("\nUsage: python3 bulk_solver.py <problems_file>")
        print("  where <problems_file> contains one problem ID per line")
        sys.exit(1)
    
    if not problems_to_solve:
        print("\nNo problems found in the input file!")
        return
    
    print(f"\nWill attempt to solve {len(problems_to_solve)} problems")
    print("=" * 70)
    
    # Process each problem
    successful = 0
    failed = []
    
    for i, problem_id in enumerate(problems_to_solve, 1):
        print(f"\n[{i}/{len(problems_to_solve)}] Processing problem {problem_id}...")
        
        try:
            # Fetch problem details
            print(f"  → Fetching problem details...")
            problem_info = fetch_problem_by_id(problem_id)
            
            if not problem_info:
                print(f"  ✗ Could not fetch problem {problem_id}")
                failed.append(problem_id)
                continue
            
            print(f"  → Title: {problem_info['title']}")
            print(f"  → Difficulty: {problem_info['difficulty']}")
            
            if dry_run:
                print(f"  → [DRY RUN] Would generate solution with GPT-5-mini")
                print(f"  → [DRY RUN] Would save to problems/{problem_id}/gpt5-mini.md")
                successful += 1
                print(f"  ✓ Problem {problem_id} validated successfully!")
                time.sleep(0.5)  # Small delay in dry run
                continue
            
            # Generate solution
            print(f"  → Generating solution with GPT-5-mini...")
            solution = generate_solution_with_ai(problem_info, api_key)
            
            if not solution:
                print(f"  ✗ Failed to generate solution for problem {problem_id}")
                failed.append(problem_id)
                continue
            
            # Save solution
            print(f"  → Saving solution...")
            saved_path = save_solution(problem_id, solution)
            
            if saved_path:
                successful += 1
                print(f"  ✓ Problem {problem_id} completed successfully!")
            else:
                failed.append(problem_id)
            
            # Rate limiting - be nice to the APIs
            if i < len(problems_to_solve):  # Don't sleep after the last problem
                time.sleep(2)  # 2 seconds between requests
                
        except Exception as e:
            print(f"  ✗ Error processing problem {problem_id}: {e}")
            failed.append(problem_id)
            continue
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Successfully processed: {successful}/{len(problems_to_solve)} problems")
    
    if failed:
        print(f"\nFailed problems: {failed}")
    else:
        print("\n✓ All problems processed successfully!")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
