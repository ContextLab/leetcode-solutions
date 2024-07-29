# [Problem 1395: Count Number of Teams](https://leetcode.com/problems/count-number-of-teams/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- Enumerating every *possible* team will take $O(n^3)$ time.  That seems long.
- I think we could do this using two sets of queues (BFS) or stacks (DFS)-- but let's try queues:
    - Initialize `nTeams = 0`.
    - One queue stores *increasing* teams and the other stores *decreasing* teams
    - First, enqueue each soldier in both queues as a single item list of indices
    - Next, for each queue type, loop until the queue is empty:
        - Dequeue the next list (at the front of the queue).  Let's say the last item in the list has index $i$.
        - For indices $i + 1$ to the end of the list of soldiers, add them to the teams if they satisfy the correct ordering.  E.g., for the increasing queue, ensure that the next item (at index $j$) is greater than the current last item at index $i$.  If the new team has length 3, increment `nTeams`.  Otherwise enqueue any newly formed "valid" teams.
    - Finally, return `nTeams`.

## Refining the problem, round 2 thoughts
- Any edge cases to consider?
    - If there are fewer than 3 soldiers, no teams are possible...but we're given that $3 \leq n \leq 1000$, so we don't need to consider this case
    - Strange `rating` values?  We're given that `ratings` are all integers.
    - We're also told that the integers in `ratings` are unique-- we could probably leverage this to implement some sort of sorting-based solution 🤔...but let's see if the queue idea works first.
- I think we can try this...

## Attempted solution(s)
```python
from collections import deque

class Solution:
    def numTeams(self, rating: List[int]) -> int:
        nTeams = 0
        increasing_queue = deque([[i] for i in range(len(rating))])
        decreasing_queue = increasing_queue.copy()

        # look for increasing teams (where rating[i] < rating[j] < rating[k])
        while len(increasing_queue) > 0:
            next_team = increasing_queue.popleft()
            for i in range(next_team[-1], len(rating)):
                if rating[i] > rating[next_team[-1]]:
                    if len(next_team) == 2:
                        nTeams += 1
                    else:
                        new_team = next_team.copy()
                        new_team.append(i)
                        increasing_queue.append(new_team)

        # now look for decreasing teams (where rating[i] > rating[j] > rating[k])
        while len(decreasing_queue) > 0:
            next_team = decreasing_queue.popleft()
            for i in range(next_team[-1], len(rating)):
                if rating[i] < rating[next_team[-1]]:
                    if len(next_team) == 2:
                        nTeams += 1
                    else:
                        new_team = next_team.copy()
                        new_team.append(i)
                        decreasing_queue.append(new_team)

        return nTeams
```
- Given test cases pass
- New test cases:
    - `rating = [4, 7, 1, 9, 10, 14, 3, 29, 1000, 950, 26, 44]`: pass
    - `rating = [62, 2, 35, 32, 4, 75, 48, 38, 28, 92, 8, 100, 68, 95, 63, 40, 42, 21, 47, 43, 89, 79, 14, 58, 85, 80, 15, 41, 10, 37, 30, 31, 24, 1, 23, 45, 53, 83, 65, 3, 49, 66, 6, 54, 34, 72, 29, 71, 52, 81, 98, 82, 18, 36, 88, 20, 12, 99, 22, 77, 97, 60, 17, 61, 27, 16, 76, 33, 69, 51, 19, 25, 46, 39, 74, 94, 67, 55, 96, 90, 93, 64, 26, 73, 87, 91, 78, 11, 5, 9, 57, 56, 50, 70, 44, 84, 86, 59, 13, 7]`: pass (note: this is a random permutation of the numbers 1...100)
- Seems ok; submitting...

![Screenshot 2024-07-28 at 11 40 23 PM](https://github.com/user-attachments/assets/40a889c6-af6e-4574-9cca-deb374176779)

Uh oh...time limit exceeded!  So: the algorithm seems correct (and even for this "failed" test case we get the right answer if I run it through "use as test case").  But this algorithm is still $O(n^3)$, which is apparently not good enough.  Let's go back to the drawing board...

## Revised thoughts (back to stream of consciousness...)
- I wonder if the sorting idea might work...or...hmmm... 🤔
- The algorithm I implemented also requires us to re-compare elements several times.  E.g., suppose we're considering building a team that includes index $i$.  If we want to build an increasing team, then *any* item from index $0...(i - 1)$ that is less than `ratings[i]` could serve as the first element, and any item from index $(i + 1)...n$ that is greater than `ratings[i]` could serve as the third element.  So if there are $a$ elements less than `ratings[i]` with indices less than `i` and $b$ elements greater than `ratings[i]` with indices greater than `i`, the total number of increasing teams is $ab$.  We can use an analogous approach to track the number of decreasing teams (just flipping the greater than/less than signs).
- Let's try something like:
    - For each element in turn (at index `i`):
        - track how many items to the left are bigger/smaller, and how many items to the right are bigger/smaller
        - the number of increasing teams we can make with element `i` as the second team member is `left_smaller * right_bigger + left_bigger * right_smaller`

New solution:
```python
class Solution:
    def numTeams(self, rating: List[int]) -> int:
        nTeams = 0
        for i in range(len(rating)):
            left_smaller, left_bigger, right_smaller, right_bigger = 0, 0, 0, 0
            for j in range(i):  # j is to the left of i
                if rating[i] > rating[j]:
                    left_smaller += 1
                else:
                    left_bigger += 1

            for j in range(i + 1, len(rating)):  # j is to the right of i
                if rating[i] > rating[j]:
                    right_smaller += 1
                else:
                    right_bigger += 1

            nTeams += left_smaller * right_bigger + left_bigger * right_smaller

        return nTeams
```
- Ok: all of the test cases, including the ones that exceeded the time limit previously are now passing
- With this algorithm I think we've gotten the runtime down to $O(n^2)$ (for filling in `left_smaller`, `left_bigger`, `right_smaller`, and `right_bigger` inside the main loop; the lefts and rights each take $O(n)$ steps to fill in, and those loops run for each element in turn (of which there are $n$).
- Submitting...

![Screenshot 2024-07-29 at 12 33 40 AM](https://github.com/user-attachments/assets/94653f0e-cce9-47d7-b43a-62192dfb2679)

🎉!
        





