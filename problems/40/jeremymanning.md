# [Problem 40: Combination Sum II](https://leetcode.com/problems/combination-sum-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- I'm thinking we could:
    - Start by sorting the list
    - Then push each value that's less than the target to a stack
    - Then use depth-first search to generate combinations (adding one element at a time, lowest to highest, until the target value is exceeded)
    - If any combination equals the target, append it to the list of combinations
        - Instead of appending it directly as a list of ints, append it as `'-'.join([str(x) for x in combo])`.  Then we can store the combinations as a set, so that no combinations are duplicated.  (At the end we'll have to convert them back to lists of ints: `return [[int(x) for x in s.split('-')] for s in combinations]`)

## Refining the problem, round 2 thoughts
- In addition to pushing (to the stack) each combination, let's also store the index of the last element in that combination.  That way we can just move forward in the list as we're considering items to append.  We can also store the current sum so that we don't have to continually loop through the combination to re-sum it.
- Open question: I'm not sure this solution is sufficiently efficient.  But we'll see...at least it's straightforward!
   
## Attempted solution(s)
```python
class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort()
        combinations = set()

        stack = []
        for i, n in enumerate(candidates):
            if n < target:
                stack.append((i, n, [n]))
            elif n == target:
                combinations.add(str(n))
            else:
                break

        while stack:
            i, combo_sum, combo = stack.pop()
            for j, n in zip(range(i + 1, len(candidates)), candidates[i + 1:]):
                x = combo_sum + n
                if x < target:
                    stack.append((j, x, [*combo, n]))
                elif x == target:
                    combinations.add('-'.join([str(x) for x in [*combo, n]]))
                else:
                    break

        return [[int(x) for x in s.split('-')] for s in combinations]
```
- Given test cases pass
- Let's make up some new test cases (using random numbers):
    - `candidates = [45, 25, 44, 9, 20, 18, 11, 27, 13, 28, 47, 50, 18, 50, 34, 25], target = 19`: pass
    - `candidates = [4, 48, 22, 11, 22, 21, 17, 50, 20, 44, 13, 43, 18, 1, 21, 44, 3, 26, 46, 21, 44, 1, 10, 9, 18, 43, 26, 40, 3, 50, 24, 38, 44, 25, 28, 8, 10, 49, 6, 34, 8, 3, 47, 26, 47, 49, 48, 1, 27, 45, 16, 35, 14, 34, 46, 5, 35, 48], target = 8`: pass
    - `candidates = [34, 23, 8, 24, 39, 32, 42, 42, 24, 14, 37, 33, 33, 7, 37, 29, 12, 24, 29, 5, 24, 48, 35, 48, 7, 17, 35, 30, 31, 47, 44, 14, 50, 10, 11, 39, 27, 5, 8, 11], target= 14`: pass
- Seems ok; submitting...

![Screenshot 2024-08-12 at 10 04 26 PM](https://github.com/user-attachments/assets/15844dee-b039-402a-b8dc-0344e651f32d)

- Ah.  Ok, so if `sum(candidates) < target` we can just return `[]`:
```python
class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        if sum(candidates) < target:
            return []
        
        candidates.sort()
        combinations = set()

        stack = []
        for i, n in enumerate(candidates):
            if n < target:
                stack.append((i, n, [n]))
            elif n == target:
                combinations.add(str(n))
            else:
                break

        while stack:
            i, combo_sum, combo = stack.pop()
            for j, n in zip(range(i + 1, len(candidates)), candidates[i + 1:]):
                x = combo_sum + n
                if x < target:
                    stack.append((j, x, [*combo, n]))
                elif x == target:
                    combinations.add('-'.join([str(x) for x in [*combo, n]]))
                else:
                    break

        return [[int(x) for x in s.split('-')] for s in combinations]
```

![Screenshot 2024-08-12 at 10 06 38 PM](https://github.com/user-attachments/assets/3bd5b19d-2dc5-4fa4-b9c8-8e22f41fec38)

- Sigh...this is getting messy 😞
- Instead of that hack (checking if the sum is less than the target), I think the actual issue here is that combinations are being duplicated many times in the depth-first search.
- Another option would be:
    - Keep track of an additional set of "combination fragments we've added so far to the stack" (using the same "hyphenated string" trick we use to track the full combinations).  And we should hold off on adding a new combination "root" if an identical fragment is already in the set.
    - On one hand, this will increase overhead.  On the other hand, it might get us over the threshold for the test cases for this specific problem 🤔
- And another "quick" thing we could try is in the initial part where we're setting up the stack-- if we've already added a number and the current index is greater than the one we've added (which it will be, since the list is sorted), don't add that new number.  We could (again) do this by keeping track of the "already tried" list (as a set)

```python
class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        if sum(candidates) < target:
            return []
        
        candidates.sort()
        combinations = set()
        tried = set()
        stack = []

        for i, n in enumerate(candidates):
            key = str(n)
            if key in tried:
                continue
            
            if n < target:
                stack.append((i, n, [n]))
                tried.add(key)
            elif n == target:
                combinations.add(key)
            else:
                break

        while stack:
            i, combo_sum, combo = stack.pop()
            for j, n in zip(range(i + 1, len(candidates)), candidates[i + 1:]):
                x = combo_sum + n
                key = '-'.join(str(c) for c in [*combo, n])

                if x > target:
                    break
                
                if x < target:
                    if key not in tried:
                        stack.append((j, x, [*combo, n]))
                        tried.add(key)
                elif x == target:
                    combinations.add(key)
                    break
        
        return [[int(x) for x in s.split('-')] for s in combinations]
```
- Given test cases pass, and so do the "failed" cases from the previous submission
- Re-submitting...

![Screenshot 2024-08-12 at 11 15 33 PM](https://github.com/user-attachments/assets/1ef50ff4-cbc9-4903-b2a5-baadbf32ce46)

Ok, I've managed to limp over the finish line.  Another successful leetcode 🙄 🥳!



