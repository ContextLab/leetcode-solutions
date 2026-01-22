#!/usr/bin/env python3
"""
Helper script to identify missing problems and create batch files for bulk solving.
"""

import os
import sys
import tempfile
from pathlib import Path


def get_problems_from_readme():
    """Extract problem numbers from README."""
    import re
    
    problems = set()
    with open('README.md', 'r') as f:
        content = f.read()
        # Match pattern like | [123](url)
        matches = re.findall(r'\| \[(\d+)\]', content)
        problems = set(int(p) for p in matches)
    
    return problems


def get_problems_with_ai_solutions():
    """Get problem IDs that have gpt5-mini.md files."""
    problems_dir = Path("problems")
    if not problems_dir.exists():
        return set()
    
    with_ai = set()
    for item in problems_dir.iterdir():
        if item.is_dir() and item.name.isdigit():
            gpt5_file = item / "gpt5-mini.md"
            if gpt5_file.exists():
                with_ai.add(int(item.name))
    
    return with_ai


def main():
    """Main function."""
    print("=" * 70)
    print("LeetCode Missing Problems Analyzer")
    print("=" * 70)
    
    # Get problems from README
    print("\nAnalyzing README...")
    readme_problems = get_problems_from_readme()
    print(f"  Found {len(readme_problems)} problems in README")
    
    # Get problems with AI solutions
    print("\nChecking for AI-generated solutions (gpt5-mini.md)...")
    problems_with_ai = get_problems_with_ai_solutions()
    print(f"  Found {len(problems_with_ai)} problems with gpt5-mini.md")
    
    # Find problems missing AI solutions
    missing_ai_solutions = sorted(readme_problems - problems_with_ai)
    
    print("\n" + "=" * 70)
    print(f"PROBLEMS MISSING AI SOLUTIONS: {len(missing_ai_solutions)}")
    print("=" * 70)
    
    if not missing_ai_solutions:
        print("\n✓ All problems in README have gpt5-mini.md files!")
        return
    
    # Show summary
    print(f"\nFirst 20: {missing_ai_solutions[:20]}")
    print(f"Last 20: {missing_ai_solutions[-20:]}")
    
    # Create temp directory for output files
    temp_dir = Path(tempfile.gettempdir())
    
    # Save to file
    output_file = temp_dir / "missing_ai_solutions.txt"
    with open(output_file, 'w') as f:
        for prob in missing_ai_solutions:
            f.write(f"{prob}\n")
    
    print(f"\n✓ Saved all {len(missing_ai_solutions)} problems to: {output_file}")
    
    # Create batch files
    batch_size = 50
    num_batches = (len(missing_ai_solutions) + batch_size - 1) // batch_size
    
    print(f"\nCreating {num_batches} batch files ({batch_size} problems each)...")
    
    for i in range(num_batches):
        start_idx = i * batch_size
        end_idx = min((i + 1) * batch_size, len(missing_ai_solutions))
        batch = missing_ai_solutions[start_idx:end_idx]
        
        batch_file = temp_dir / f"batch_{i+1:03d}.txt"
        with open(batch_file, 'w') as f:
            for prob in batch:
                f.write(f"{prob}\n")
        
        print(f"  Batch {i+1:3d}: {len(batch):2d} problems -> {batch_file}")
    
    print("\n" + "=" * 70)
    print("To solve problems locally (if you have OPENAI_API_KEY):")
    print(f"  python3 auto_solver.py --bulk {temp_dir}/batch_001.txt")
    print("\nTo solve via GitHub Actions:")
    print("  Manually trigger the 'Bulk Solve Missing LeetCode Problems' workflow")
    print("=" * 70)


if __name__ == "__main__":
    main()
