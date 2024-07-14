# [Problem 726: Number of Atoms](https://leetcode.com/problems/number-of-atoms/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- We are not dealing with super long formulas, so we can afford to be a little inefficient (if needed)
- I think we should start by "tokenizing" the formula by splitting it into:
    - Elements (capital letter followed by 0+ lowercase letters)
    - Numbers (consecutive sequences of digits; convert these to integers)
    - Parentheses
- Tokenizing will allow us to do bookkeeping more easily
- I also think it'd be worth doing a first pass to identify the positions of all the parentheses.  In $O(n)$ time we could start a counter at 0 and then move through the string character by character.  Each time we hit a "(" we increment the counter and add the position to a hash table (key: counter value?  position?; value: could either be the position of the matching closing parentheses, or a list where the first element is the position of the open parenthesis and the second element is the position of the matching close parenthesis).  If we hit a ")" we decrement the counter and update the hash table accordingly.  This will let us easily do recursion later:
    - When we're doing the main processing, if we hit "(" we can get from the hash table the entire contents (up to its matching ")"), run our helper counting function on that sub-string, and then add it to our running total.  (The running total, btw, should also be stored in a hash table.  Aside: I'm not sure if dicts can be added, or how that works if they don't have exactly the same keys; need to figure this out...)
    - Once we've finished processing the content inside the parentheses, we can skip ahead to after the parentheses
    - This will save a lot of time, because we won't have to keep scanning forward (potentially recursively) to match up parentheses
    - Note: the "helper" function (i.e., the function called recursively) will need to have an "offset" parameter (default: 0) to enable us to avoid needing to re-compute the parenthesis matching each time we enter a new recursion depth.  E.g. something like `close_pos = parens[i + offset] - offset`.  And then if we encounter nested parentheses, we'd need to pass in `offset = i + offset` to the recursion call.
- Then I think the basic approach is straightforward:
    - Tokenize the string
    - Create a hash table for the parentheses pairings
    - Start a hash table with the atom counts:
        - This could either be created during the tokenization process (e.g., whenever an element is found, add a key for that element and initialize its count to 0), or we could just initialize the hash table to an empty dict and add new elements as needed if they haven't already been accounted for.
    - Set `current` to `{}` (used to process digits)
    - Then go through each token one by one:
        - If we encounter an element (`x`):
            - Add `current` to the running totals
            - update `current` to `{x: 1}`
        - If we encounter a number (`i`):
            - Multiply every value in `current` by `i`
            - Add `current` to the running totals
            - Reset `current` to `{}`
        - If we encounter a parenthesis:
            - `current = helper(<get contents of parens>, offset=i + offset)`
    - At the end of the helper function, add `current` to the total and then return the total counts (a dict)
    - Finally, put the output in the right format:
        - Let's say that `counts` is the element-wise counts
        - `counts = sorted([[key, val] for key, val in counts.items], key=lambda x: x[0])`
        - `return ''.join([f'{x[0]x[1]}' if x[1] > 1 else x[0] for x in counts])`

## Refining the problem, round 2 thoughts
- Some helper functions are needed:
    - Tokenize the formula-- take in the formula and return a list of tokens
        - This might have some tricky parts to it
        - What I'm imagining is that we initialize `t` (current token) to an empty string and then go through character by character (current character: `c`):
            - If `c in "()"`:
                - append `c` to the current list of parsed tokens
                - set `t = ''`
            - If `c` is a capital letter:
                - if `len(t) > 0`:
                    - if `t[0]` is a digit:
                        - `t = int(t)`
                        - append `t` to the current list of parsed tokens
                    - otherwise, if `t[0]` is a lowercase or capital letter, append `t` to the current list of parsed tokens
                    - reset `t` to `''`
                - set `t = c`
            - If `c` is a lowercase letter, `t += c`
            - If `c` is a digit:
                - If `len(t) > 0`:
                    - If `t[-1]` is also a digit, `t += c`
                    - Else:
                        - Append `t` to the current list of parsed tokens
                        - Set `t = c`
                - Otherwise `t = c`
        - At the end, make sure to add `t` to the list of tokens if it's not empty.  (If it's a digit, convert to an `int` first.)
        - Then just return the list of parsed tokens
    - Parenthesis matching function
        - A potentially tricky case could arise, whereby the "depth" for several parenthesis pairs is the same.  E.g., for the formula "X(XX)XXX(XX)XXXX..." both parenthesis pairs have the same depth.  I think a hash table is still the "right" way to handle parenthesis matching, but instead of using 2-element lists of ints, maybe we should instead use lists of 2-element lists.  Then as we use each new pair, we'll just dequeue it from the front of that entry in the hash table so that we don't need to continually match up the current position with all of the entries.
    - Add two dicts, potentially with mismatched keys-- take in two count dicts and return a single "merged" count dict
    - Multiply a dict by a constant-- take in a count dict and an integer and return a new count dict with updated values
    - Main helper function-- take in a list of tokens and an offset (default: 0) and return a count dict
- I might be missing an edge case...but if not, nothing here is too crazy.  There are just a bunch of pieces to this problem (more than the usual short solutions).

## Attempted solution(s)
```python
import collections  # thanks for pointing me to this, Paxton!!

class Solution:
    def countOfAtoms(self, formula: str) -> str:        
        def tokenize(formula):
            tokens = []
            i = 0
            n = len(formula)
            while i < n:
                if formula[i].isupper():
                    start = i
                    i += 1
                    while i < n and formula[i].islower():
                        i += 1
                    tokens.append(formula[start:i])
                elif formula[i].isdigit():
                    start = i
                    i += 1
                    while i < n and formula[i].isdigit():
                        i += 1
                    tokens.append(int(formula[start:i]))
                elif formula[i] in "()":
                    tokens.append(formula[i])
                    i += 1
            return tokens
        
        def multiply_dict(d, factor):
            for key in d:
                d[key] *= factor
            return d
        
        def merge_dicts(d1, d2):
            for key in d2:
                if key in d1:
                    d1[key] += d2[key]
                else:
                    d1[key] = d2[key]
            return d1
        
        def count_atoms(tokens, offset=0):
            total_count = collections.defaultdict(int)
            i = offset
            while i < len(tokens):
                if isinstance(tokens[i], str) and tokens[i].isalpha():
                    elem = tokens[i]
                    count = 1
                    if i + 1 < len(tokens) and isinstance(tokens[i + 1], int):
                        count = tokens[i + 1]
                        i += 1
                    total_count[elem] += count
                elif tokens[i] == "(":
                    depth = 1
                    j = i + 1
                    while j < len(tokens) and depth > 0:
                        if tokens[j] == "(":
                            depth += 1
                        elif tokens[j] == ")":
                            depth -= 1
                        j += 1
                    sub_count = count_atoms(tokens, i + 1)
                    i = j - 1
                    if i + 1 < len(tokens) and isinstance(tokens[i + 1], int):
                        count = tokens[i + 1]
                        i += 1
                    else:
                        count = 1
                    multiply_dict(sub_count, count)
                    merge_dicts(total_count, sub_count)
                elif tokens[i] == ")":
                    return total_count
                i += 1
            return total_count

        tokens = tokenize(formula)
        atom_counts = count_atoms(tokens)

        sorted_atoms = sorted(atom_counts.items())
        result = []
        for atom, count in sorted_atoms:
            result.append(atom)
            if count > 1:
                result.append(str(count))

        return ''.join(result)
```
- Given test cases: pass
- Need to stop for today, so no time to test other cases...just submitting

![Screenshot 2024-07-14 at 2 45 53 PM](https://github.com/user-attachments/assets/fc8ff425-12c8-4ee0-af6f-450e3f627118)
- meh...
- maybe a stack would have been better than a recursive solution?  would have avoided copying...

