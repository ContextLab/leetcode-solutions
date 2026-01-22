# Bulk Solution Generation for Missing LeetCode Problems

This document describes the tools and processes for systematically adding AI-generated solutions to all LeetCode problems in the repository.

## Problem Statement

The repository tracks 548 LeetCode problems (as listed in README.md), but many lack AI-generated solutions:
- **76 problems** have `gpt5-mini.md` files (AI-generated solutions)
- **472 problems** are missing AI-generated solutions

Some problems have only human-generated solutions (e.g., `jeremymanning.md`), and we want to add AI solutions for all of them.

## Tools Provided

### 1. `identify_missing.py`

Analyzes the repository to identify which problems are missing AI-generated solutions.

**Usage:**
```bash
python3 identify_missing.py
```

**What it does:**
- Scans README.md to find all problem numbers
- Checks for existence of `problems/*/gpt5-mini.md` files
- Reports which problems are missing AI solutions
- Creates batch files for processing (50 problems per batch)
- Saves results to `/tmp/missing_ai_solutions.txt` and `/tmp/batch_*.txt`

### 2. `bulk_solver.py`

Generates AI solutions for a list of problems using OpenAI's GPT-5-mini model.

**Usage:**
```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"

# Process a batch of problems
python3 bulk_solver.py /tmp/batch_001.txt

# Or test without API key (dry run)
python3 bulk_solver.py /tmp/batch_001.txt --dry-run
```

**What it does:**
- Reads problem IDs from input file (one per line)
- Fetches problem details from LeetCode API
- Generates solutions using GPT-5-mini
- Saves solutions as `problems/{id}/gpt5-mini.md`
- Handles rate limiting (2 seconds between requests)
- Reports success/failure for each problem

**Features:**
- Dry-run mode for testing without API key
- Detailed progress reporting
- Error handling and retry logic
- Respects API rate limits

### 3. GitHub Actions Workflow: `bulk_solver.yml`

Automated workflow for bulk solving problems via GitHub Actions.

**Location:** `.github/workflows/bulk_solver.yml`

**How to use:**
1. Go to the repository's Actions tab
2. Select "Bulk Solve Missing LeetCode Problems"
3. Click "Run workflow"
4. Configure:
   - **batch_size**: Number of problems to solve (default: 50)
   - **start_index**: Which problem to start from (default: 0)
5. Click "Run workflow" to start

**What it does:**
- Automatically identifies missing AI solutions
- Processes a batch of problems
- Commits and pushes generated solutions
- Can be run multiple times with different start_index values

**Example workflow runs:**
- Run 1: start_index=0, batch_size=50 → solves problems 1-50
- Run 2: start_index=50, batch_size=50 → solves problems 51-100
- Run 3: start_index=100, batch_size=50 → solves problems 101-150
- etc.

## Workflow for Adding All Missing Solutions

### Option A: Using GitHub Actions (Recommended)

1. **Initial Analysis**
   ```bash
   python3 identify_missing.py
   ```
   This shows you how many problems need solutions (currently 472).

2. **Trigger Workflow Runs**
   - Go to Actions → "Bulk Solve Missing LeetCode Problems"
   - Run workflow with: start_index=0, batch_size=50
   - Wait for completion, then run again with: start_index=50, batch_size=50
   - Repeat until all problems are processed (10 runs total for 472 problems)

3. **Monitor Progress**
   - Check the Actions tab for workflow status
   - Solutions will be automatically committed to main branch

### Option B: Using Local Script (If you have OpenAI API key)

1. **Setup**
   ```bash
   # Install dependencies
   pip install requests openai httpx
   
   # Set API key
   export OPENAI_API_KEY="your-key-here"
   ```

2. **Generate batch files**
   ```bash
   python3 identify_missing.py
   ```

3. **Process batches**
   ```bash
   # Process first batch
   python3 bulk_solver.py /tmp/batch_001.txt
   
   # Commit changes
   git add problems/*/gpt5-mini.md
   git commit -m "Add AI solutions for batch 1"
   git push
   
   # Continue with remaining batches...
   python3 bulk_solver.py /tmp/batch_002.txt
   # ... and so on
   ```

## Solution Format

All AI-generated solutions follow this format:

```markdown
# [Problem {ID}: {Title}]({URL})

## Initial thoughts (stream-of-consciousness)
[Initial analysis and approach]

## Refining the problem, round 2 thoughts
[Refined approach, edge cases, complexity analysis]

## Attempted solution(s)
\`\`\`python
[Complete Python solution]
\`\`\`
- [Notes about approach and complexity]
```

## Technical Details

### API Rate Limiting
- The script includes 2-second delays between requests
- This prevents overwhelming the LeetCode or OpenAI APIs
- For 472 problems, expect ~15-20 minutes per batch of 50

### Error Handling
- Problems that fail to fetch are skipped and logged
- Failed problems are reported at the end
- You can re-run with just the failed problems

### Network Requirements
- Requires access to `leetcode.com` (for problem details)
- Requires access to OpenAI API (for solution generation)
- GitHub Actions environment has these by default

## Monitoring Progress

After running batches, you can check progress:

```bash
# Count AI solutions
find problems -name "gpt5-mini.md" | wc -l

# Re-run analysis
python3 identify_missing.py
```

## Notes

- The existing `auto_solver.py` handles daily problems automatically
- This bulk solver is for backfilling historical problems
- Both use the same GPT-5-mini model and format
- Solutions are idempotent - safe to re-run if a problem already has gpt5-mini.md
