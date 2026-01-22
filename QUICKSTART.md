# Quick Start Guide: Adding Missing AI Solutions

## For Repository Maintainers

### Option 1: Using GitHub Actions (Recommended)

This is the easiest way to add solutions for all 472 missing problems:

1. **Navigate to Actions**
   - Go to the repository on GitHub
   - Click the "Actions" tab

2. **Select the Workflow**
   - Click "Bulk Solve Missing LeetCode Problems" in the left sidebar

3. **Run the Workflow**
   - Click "Run workflow" button
   - Keep default settings:
     - `batch_size`: 50 (processes 50 problems)
     - `start_index`: 0 (starts from first missing problem)
   - Click "Run workflow"

4. **Monitor Progress**
   - The workflow takes ~15-20 minutes per batch
   - Check the Actions tab to see when it completes
   - Solutions will be automatically committed to main branch

5. **Run Next Batch**
   - After first batch completes, run again with:
     - `batch_size`: 50
     - `start_index`: 50
   - Continue incrementing `start_index` by 50 for each run
   - Total of 10 runs needed to complete all 472 problems

### Option 2: Using Local Script (If you have OpenAI API access)

```bash
# 1. Set up environment
export OPENAI_API_KEY="your-api-key-here"
pip install requests openai httpx

# 2. Identify missing problems
python3 identify_missing.py

# 3. Process first batch
python3 bulk_solver.py /tmp/batch_001.txt

# 4. Commit and push
git add problems/*/gpt5-mini.md
git commit -m "Add AI solutions for batch 1"
git push

# 5. Repeat for remaining batches
python3 bulk_solver.py /tmp/batch_002.txt
# ... and so on
```

## Expected Timeline

- **Per batch (50 problems)**: ~15-20 minutes
- **All 472 problems**: ~3-4 hours total (split across 10 batch runs)
- **Manual effort**: ~5 minutes per batch (just triggering workflow)

## Verification

Check progress at any time:

```bash
# Count AI solutions
find problems -name "gpt5-mini.md" | wc -l

# Re-analyze to see remaining
python3 identify_missing.py
```

## What Gets Created

For each problem, a file `problems/{ID}/gpt5-mini.md` is created containing:
- Problem title and link
- Initial thoughts and approach
- Refined analysis with complexity considerations
- Complete Python solution with explanations

All solutions follow the same format as existing `gpt5-mini.md` files.

## Troubleshooting

**Problem: Workflow fails with "OPENAI_API_KEY not set"**
- Solution: Ensure the repository has the `OPENAI_API_KEY` secret configured in Settings → Secrets

**Problem: Some problems fail to fetch**
- Solution: These are skipped and logged. You can retry failed problems by creating a custom batch file

**Problem: Rate limiting errors**
- Solution: The script includes built-in 2-second delays. If issues persist, reduce `batch_size`

## Support

See `BULK_SOLVER_README.md` for detailed documentation on all features and options.
