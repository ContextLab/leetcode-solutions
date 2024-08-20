# [Problem 1140: Stone Game II](https://leetcode.com/problems/stone-game-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- This one seems tricky...I'm sort of surprised it's a "Medium" problem.  There must be a relatively straightforward solution, just based on its difficulty rating.
- I'm assuming (based on recent problems) that there's a dynamic programming approach.  It'll probably look something like:
    - `score[i]` stores the maximum number of stones Alice can accumulate through turn `i`.  And then the *next* entry must be computable using some function of `score[i]`.  Some unknowns:
        - Do we also need a dynamic programming "tracker" for Bob's moves?
        - I'm also not sure what the function should even look like
- What *do* we know?
    - Alice can take either 1 or 2 piles initially.  So if `len(piles) <= 2`, then we can just return `sum(piles)`.
    - Beyond that...let's see...we should (obviously) try to maximize Alice's score while minimizing Bob's score.  But how can we do that?
        - I'm not sure if this will factor into the actual solution, but in the given examples, it seems like there are two scenarios that seem potentially prototypical:
            - If all of the values are sort of similar, then we should just try to maximize the number of piles Alice gets.  Note: we'll need to come back to *how* this might be done.
            - If there's a single pile with a much bigger value, then we should do what we can to get *that* pile.  Again, I'm not sure how we might do that.
        - Hmmm.  What might a "brute force" solution look like?
            - We could do a breadth-first search:
                - Initialize Alice's max score to 0
                - start the queue with both of Alice's possible moves (let's have each element also store the current value of `M`, Bob's score, and the position of the next stone).  Either she can take only pile 1, or both piles 1 and 2
                - For each subsequent move (until the queue is empty):
                    - Note: I'm not sure yet how we should handle Bob's moves.  Do we want a separate queue for Bob?  Or can we put him in the same queue and then track whose turn it is?
                    - Dequeue the front of the queue and enqueue all of the possible next turns (if any)
                    - When there are no possible moves left for the given move sequence, set Alice's max score to the max of the current max and the new sequence's score
                - Then just return Alice's maximum score
            - We could use also build this as a depth-first search by changing the queue to a stack
            - It's certainly not efficient to do this...but on the other hand, maybe it'll be OK since the maximum number of piles is 100?
- If we pursue this approach, I'm guessing we're going to run up against a "time limit exceeded" error.  At the same time, I can't think of another obvious approach off the top of my head.  So let's go with it, and then see if it passes.

## Refining the problem, round 2 thoughts
- There are a few things to solve:
    - First, how should moves be enqueued?
        - We could potentially store moves as dictionaries:
            - Turn: whose turn is it next?  ("A" or "B")
            - Alice's total score
            - Index of the next-to-be-considered pile
            - Current value of `M`
        - Well actually, that's not *so* bad-- we could just represent this as a simple list, like `player, alice_score, i, M = ["A", 20, 5, 2]`
    - Second, should we maintain separate queues for Alice and Bob?  I don't think so-- since we have a representation of whose turn it is already (using the above implementation), we'll just need to enqueue both Bob's and Alice's turns using the same queue.
    - I don't think it'll end up mattering much if we use a breadth-first or depth-first search.  Let's just go with breadth-first (why not?).  We can use a `dequeue` object to support fast pops from the front of the queue.
- Another unknown: how do we ensure that *Bob* plays optimally?  I'm wondering if we should update Alice's max score only if Bob's moves up to that point also maximize *his* score.  But...that's not quite right, because Alice gets to go first.  I'm not sure how to deal with this.  I'm going to ignore this temporarily, with the recognition that we'll likely get some answers wrong.  I'm hoping this can be caught in testing before I submit.
- In any case...let's try it!

## Attempted solution(s)
```python
from collections import deque

class Solution:
    def stoneGameII(self, piles: List[int]) -> int:
        max_score = 0
        if len(piles) <= 2:
            return sum(piles)

        moves = deque([("B", piles[0], 1, 1), ("B", sum(piles[:2]), 2, 2)])
        while moves:
            current_player, score, i, M = moves.popleft()
            if i >= len(piles):
                max_score = max(max_score, score)
                continue
            
            if current_player == "A":
                next_player = "B"
            else:
                next_player = "A"

            X = 0
            for j in range(i, min(i + 2 * M + 1, len(piles))):
                X += 1
                if current_player == "A":
                    score += piles[j]
                moves.append((next_player, score, j + 1, max(M, X)))

        return max_score
```
- Ok...this is giving the wrong answers for both of the given examples.  I'm thinking there are a few issues:
    - I'm still pretty sure this is too inefficient.  So...even if I get it working, it'll still likely not work
    - This approach doesn't optimize *Bob's* moves.  I think that's what the issue here is.
- My "gut" is that (like I mentioned in my initial thoughts) there's likely to be a dynamic programming solution to this.  We'll need some function `maximize_score(i, M)` that maximizes the score starting from pile `i`, with the given value of `M`.  Then we'll need to find some way of "reusing computations" by finding `maximize_score(j, new_M)` for $j > i$, given `maximize_score(i, M)`.  There will be lots of re-used computations, so we'll need a hash table or similar to save the max scores for each position.
    - This would also let us simultaneously optimize Alice's and Bob's scores-- essentially we want to know how many stones one player can get, and the remaining stones will go to the other player.  These can be computed by asking:
        - How many stones are there left (in the remaining piles) after pile `i`?
        - What's the max achievable score starting from pile `i`, given `M`?
- Let's try this...
```python
class Solution:
    def stoneGameII(self, piles: List[int]) -> int:
        # first compute the number of stones remaining, starting from position i
        remaining = [0] * len(piles)
        remaining[-1] = piles[-1]
        for i in range(len(piles) - 2, -1, -1):
            remaining[i] = remaining[i + 1] + piles[i]

        # start a cache
        cache = {}

        # define the maximize_score function
        def maximize_score(i, M):
            # already collected the last pile?
            if i >= len(piles):
                return 0

            # already computed?
            if (i, M) in cache:
                return cache[(i, M)]

            # do the work...
            stones = 0
            for X in range(1, 2 * M + 1):
                if i + X <= len(piles):
                    # pick the max between...
                    # option 1: what we've already collected
                    # option 2: all remaining stones except whatever the other player can (maximally) collect from the remaining piles
                    stones = max(stones, remaining[i] - maximize_score(i + X, max(M, X)))
            cache[(i, M)] = stones
            return stones

        # just maximize the score for the first move (which is Alice's, by definition)
        return maximize_score(0, 1)    
```
- Great, given test cases pass!
- Let's try some others...
    - `piles = [1, 8168, 33, 5414, 9711, 5564, 1428, 2427, 7513, 9081, 3128, 7708, 6822, 858, 7406, 288, 5390, 5670, 9507, 5556, 4452, 1542, 525, 6223, 3839, 498, 5924, 4971, 4594, 1580, 3849, 8261, 4955, 2528, 6023, 2006, 2469, 6165, 5737, 5405, 4702, 2971, 4448, 3363, 8617, 5516, 2569, 9153, 4014, 3836, 656, 9594, 1572, 7157, 2961, 9234, 5175, 7570, 5518, 6656, 5731, 572, 3800, 5964, 4153, 3035, 887, 904, 470, 3636, 202, 4085, 4631, 6983, 1464, 4407, 1105, 6009, 3107, 7063, 9950, 3952, 3367, 2342, 6028, 7579, 5892, 2908, 3977, 6930, 2212, 9465, 9933, 1809, 7359, 790, 8383, 5187, 6471, 4048]`: pass (so...we're probably good, but for kicks let's try another also)
    - `piles = [4997, 3371, 505, 9687, 1343, 6480, 7798, 5756, 2034, 4628, 597, 4217, 9076, 1898, 8450, 99, 7843, 1539, 6546, 1760, 5541, 8832, 1795, 7707, 9128, 4716, 3355, 713, 3726, 219, 7396, 7667, 3141, 1336, 1316, 8931, 9100, 9414, 8401, 9958, 7069, 653, 8297, 178, 4968, 6541, 8409, 4736, 9620, 1667, 4508, 3842, 1650, 7707, 8403, 2714, 8310, 6107, 8729, 8381, 8657, 3158, 8997, 5616, 8721, 7826, 7543, 3144, 5755, 5473, 5242, 934, 4713, 8718, 1585, 4687, 7344, 5119, 552, 36, 615, 5502, 283, 9370, 8944, 8719, 4551, 116, 7375, 7509, 3225, 5372, 5960, 2657, 1136, 1924, 7458, 4692, 303, 9060]`: pass
- Let's submit...

![Screenshot 2024-08-19 at 11 35 19 PM](https://github.com/user-attachments/assets/503639ed-72be-44fa-8239-9f5b4e6f0302)

Solved!


