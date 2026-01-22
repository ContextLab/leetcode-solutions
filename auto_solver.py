#!/usr/bin/env python3
"""
Auto-solver for daily LeetCode problems using OpenAI GPT-5-mini.
This script fetches the daily problem (or a specific problem by ID), uses AI to solve it, and creates a solution file.

Usage:
    python3 auto_solver.py              # Solve today's daily problem
    python3 auto_solver.py 123          # Solve problem #123
    python3 auto_solver.py --bulk file.txt  # Solve all problems in file (one ID per line)
"""

import os
import sys
import json
import requests
import time
from datetime import datetime
from openai import OpenAI


# Global cache for problem ID to titleSlug mapping
_problem_cache = None


def _build_problem_cache():
    """
    Build a cache of all problem IDs to their titleSlugs by paginating through
    the entire LeetCode problem set.

    Returns:
        dict: Mapping of problem ID (str) to titleSlug
    """
    global _problem_cache
    if _problem_cache is not None:
        return _problem_cache

    leetcode_api_url = "https://leetcode.com/graphql"
    _problem_cache = {}

    # Fetch all problems using pagination
    # We'll fetch in batches, but use a larger limit and no category filter
    # to ensure we get ALL problems
    query = {
        "query": """query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
            problemsetQuestionList: questionList(
                categorySlug: $categorySlug
                limit: $limit
                skip: $skip
                filters: $filters
            ) {
                total: totalNum
                questions: data {
                    questionFrontendId
                    title
                    titleSlug
                    difficulty
                }
            }
        }""",
        "variables": {
            "categorySlug": "",
            "skip": 0,
            "limit": 100,
            "filters": {},
        },
        "operationName": "problemsetQuestionList",
    }

    skip = 0
    batch_size = 100
    total_fetched = 0
    total_problems = None

    print("  Building problem cache (fetching all problems from LeetCode)...")

    while True:
        query["variables"]["skip"] = skip

        try:
            response = requests.post(leetcode_api_url, json=query, timeout=60)
            response.raise_for_status()
            data = response.json()

            if "data" in data and "problemsetQuestionList" in data["data"]:
                result = data["data"]["problemsetQuestionList"]
                questions = result["questions"]

                if total_problems is None:
                    total_problems = result.get("total", 0)
                    print(f"    Total problems in LeetCode: {total_problems}")

                if not questions:
                    break

                for q in questions:
                    _problem_cache[str(q["questionFrontendId"])] = {
                        "titleSlug": q["titleSlug"],
                        "title": q["title"],
                        "difficulty": q["difficulty"],
                    }

                total_fetched += len(questions)
                print(f"    Fetched {total_fetched}/{total_problems} problems...")

                if len(questions) < batch_size:
                    break

                skip += batch_size
                time.sleep(0.5)  # Small delay to avoid rate limiting
            else:
                print(f"    Unexpected response structure during cache build")
                break

        except Exception as e:
            print(f"    Error during cache build at skip={skip}: {e}")
            break

    print(f"  Problem cache built with {len(_problem_cache)} problems")
    return _problem_cache


def fetch_problem_by_id(problem_id):
    """
    Fetch a specific LeetCode problem by its ID using the GraphQL API.

    Args:
        problem_id (str): The problem ID (e.g., "1", "2", "100")

    Returns:
        dict: Problem details or None if not found
    """
    # Build or retrieve the problem cache
    cache = _build_problem_cache()

    problem_id_str = str(problem_id)

    if problem_id_str in cache:
        cached_info = cache[problem_id_str]
        # Fetch full details including content
        return fetch_problem_details(cached_info["titleSlug"])

    print(
        f"Problem {problem_id} not found in LeetCode database (checked {len(cache)} problems)"
    )
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
        "operationName": "questionData",
    }

    try:
        response = requests.post(leetcode_api_url, json=query, timeout=30)
        response.raise_for_status()
        data = response.json()

        if "data" in data and "question" in data["data"]:
            question = data["data"]["question"]
            return {
                "problem_id": question["questionFrontendId"],
                "title": question["title"],
                "title_slug": question["titleSlug"],
                "difficulty": question["difficulty"],
                "content": question["content"],
                "link": f"https://leetcode.com/problems/{question['titleSlug']}/description/?envType=daily-question",
            }
        else:
            print(f"Error: Could not fetch details for {title_slug}")
            return None

    except Exception as e:
        print(f"Error fetching problem details for {title_slug}: {e}")
        return None


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
        "operationName": "questionOfToday",
    }

    try:
        response = requests.post(leetcode_api_url, json=daily_challenge_query)
        response.raise_for_status()
        data = response.json()

        if "data" in data and "activeDailyCodingChallengeQuestion" in data["data"]:
            problem_data = data["data"]["activeDailyCodingChallengeQuestion"]
            question = problem_data["question"]

            return {
                "problem_id": question["questionFrontendId"],
                "title": question["title"],
                "title_slug": question["titleSlug"],
                "difficulty": question["difficulty"],
                "content": question["content"],
                "link": f"https://leetcode.com/problems/{question['titleSlug']}/description/?envType=daily-question",
                "example_testcases": question.get("exampleTestcases", ""),
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
        import httpx

        # Create an httpx client that doesn't verify SSL certificates
        # This is needed when running behind a proxy with self-signed certificates
        http_client = httpx.Client(verify=False)
        client = OpenAI(api_key=api_key, http_client=http_client)

        # Create a detailed prompt for the AI
        prompt = f"""You are solving a LeetCode problem. Generate a complete solution following this exact format:

# [Problem {problem_info["problem_id"]}: {problem_info["title"]}]({problem_info["link"]})

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

**Title:** {problem_info["title"]}
**Difficulty:** {problem_info["difficulty"]}
**Link:** {problem_info["link"]}

**Problem Description:**
{problem_info["content"]}

Please provide a thoughtful, well-explained solution that demonstrates clear problem-solving skills. The solution should be efficient and include proper complexity analysis."""

        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert software engineer solving LeetCode problems. Provide clear explanations and efficient solutions.",
                },
                {"role": "user", "content": prompt},
            ],
            max_completion_tokens=8000,
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

        with open(solution_file, "w", encoding="utf-8") as f:
            f.write(solution_content)

        print(f"Solution saved to: {solution_file}")
        return solution_file

    except Exception as e:
        print(f"Error saving solution: {e}")
        return None


def main():
    """Main execution function."""
    # Check for bulk mode
    if len(sys.argv) >= 3 and sys.argv[1] == "--bulk":
        # Bulk mode: solve multiple problems from file
        bulk_solve(sys.argv[2])
        return

    # Check for specific problem ID
    if len(sys.argv) >= 2 and sys.argv[1].isdigit():
        # Single problem mode by ID
        problem_id = sys.argv[1]
        solve_problem_by_id(problem_id)
        return

    # Default: daily problem mode
    solve_daily_problem()


def solve_daily_problem():
    """Solve today's daily problem."""
    print("=" * 60)
    print("LeetCode Auto-Solver - Daily Problem Mode")
    print("=" * 60)

    # Get OpenAI API key from environment
    api_key = os.environ.get("OPENAI_API_KEY")
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

    # Generate and save solution
    generate_and_save_solution(problem_info, api_key)


def solve_problem_by_id(problem_id):
    """Solve a specific problem by ID."""
    print("=" * 60)
    print(f"LeetCode Auto-Solver - Problem #{problem_id}")
    print("=" * 60)

    # Get OpenAI API key from environment
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        sys.exit(1)

    # Fetch problem
    print(f"\n1. Fetching problem {problem_id}...")
    problem_info = fetch_problem_by_id(problem_id)
    if not problem_info:
        print(f"Failed to fetch problem {problem_id}")
        sys.exit(1)

    print(f"   Title: {problem_info['title']}")
    print(f"   Difficulty: {problem_info['difficulty']}")

    # Generate and save solution
    generate_and_save_solution(problem_info, api_key)


def bulk_solve(problems_file):
    """Solve multiple problems from a file."""
    print("=" * 60)
    print("LeetCode Auto-Solver - Bulk Mode")
    print("=" * 60)

    # Get OpenAI API key from environment
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        sys.exit(1)

    # Read problem IDs from file
    print(f"\nReading problems from: {problems_file}")
    try:
        with open(problems_file, "r") as f:
            problem_ids = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    print(f"Found {len(problem_ids)} problems to solve\n")

    # Process each problem
    successful = 0
    failed = []

    for i, problem_id in enumerate(problem_ids, 1):
        print(f"\n[{i}/{len(problem_ids)}] Processing problem {problem_id}...")

        try:
            # Fetch problem
            print(f"  → Fetching problem details...")
            problem_info = fetch_problem_by_id(problem_id)

            if not problem_info:
                print(f"  ✗ Could not fetch problem {problem_id}")
                failed.append(problem_id)
                continue

            print(f"  → Title: {problem_info['title']}")
            print(f"  → Difficulty: {problem_info['difficulty']}")

            # Generate solution
            print(f"  → Generating solution with GPT-5-mini...")
            solution = generate_solution_with_ai(problem_info, api_key)

            if not solution:
                print(f"  ✗ Failed to generate solution")
                failed.append(problem_id)
                continue

            # Save solution
            print(f"  → Saving solution...")
            saved_path = save_solution(problem_info["problem_id"], solution)

            if saved_path:
                successful += 1
                print(f"  ✓ Problem {problem_id} completed successfully!")
            else:
                failed.append(problem_id)

            # Rate limiting
            if i < len(problem_ids):
                time.sleep(2)  # 2 seconds between requests

        except Exception as e:
            print(f"  ✗ Error: {e}")
            failed.append(problem_id)
            continue

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Successfully processed: {successful}/{len(problem_ids)} problems")
    if failed:
        print(f"\nFailed problems: {failed}")
    else:
        print("\n✓ All problems processed successfully!")
    print("=" * 60)


def generate_and_save_solution(problem_info, api_key):
    """Generate and save a solution for a problem."""
    # Generate solution
    print("\n2. Generating solution with GPT-5-mini...")
    solution = generate_solution_with_ai(problem_info, api_key)
    if not solution:
        print("Failed to generate solution")
        sys.exit(1)

    print("   Solution generated successfully!")

    # Save the solution
    print("\n3. Saving solution to file...")
    saved_path = save_solution(problem_info["problem_id"], solution)
    if not saved_path:
        print("Failed to save solution")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("Auto-solver completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
