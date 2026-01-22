# [Problem 2353: Design a Food Rating System](https://leetcode.com/problems/design-a-food-rating-system/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need a data structure that supports two operations: change the rating of a food, and return the highest-rated food for a given cuisine (breaking ties by lexicographic order). The highestRated operation must be efficient and updates happen often. A max-structure per cuisine is required.

Python doesn't have a built-in max-heap nor a tree-set keyed by custom ordering. A natural choice is to use a heap (min-heap with negative ratings) per cuisine and do lazy deletions: when a food's rating changes, push the new (-rating, food) tuple into that cuisine's heap. On highestRated, pop stale entries until the top matches the current rating in a centralized food->rating map. That yields good amortized complexity and is straightforward to implement.

Alternative would be a balanced BST or sorted list per cuisine keyed by (-rating, name) to allow removals and inserts in O(log n) — doable in other languages or with external libraries, but lazy heaps are simplest in Python.

## Refining the problem, round 2 thoughts
- Maintain:
  - food_to_cuisine: map food -> cuisine (string)
  - food_to_rating: map food -> current rating (int)
  - cuisine_to_heap: map cuisine -> list used as heap of tuples (-rating, food)
- Initialization: push every food into its cuisine heap.
- changeRating(food, newRating): update food_to_rating[food] and push (-newRating, food) onto the cuisine heap (lazy update).
- highestRated(cuisine): while top of cuisine heap is stale (i.e., -rating != current rating or food's cuisine doesn't match), pop. The valid top is the answer.

Edge cases:
- All foods are distinct so heap entries are identified by name + rating tuple.
- The constraints guarantee queries are valid (food exists and cuisine exists).
- Complexity:
  - Initialization: O(n log n) due to pushes.
  - changeRating: O(log n) per push.
  - highestRated: amortized O(log n) because each stale entry is popped at most once; worst-case single call could pop many but total pops bounded by total pushes.
- Space: O(n + number of updates) heap entries across all heaps; still O(n + q) overall.

## Attempted solution(s)
```python
import heapq

class FoodRatings:
    def __init__(self, foods, cuisines, ratings):
        # Map food -> cuisine
        self.food_to_cuisine = {}
        # Map food -> current rating
        self.food_to_rating = {}
        # Map cuisine -> heap of (-rating, food)
        self.cuisine_to_heap = {}
        
        for f, c, r in zip(foods, cuisines, ratings):
            self.food_to_cuisine[f] = c
            self.food_to_rating[f] = r
            if c not in self.cuisine_to_heap:
                self.cuisine_to_heap[c] = []
            # Use (-rating, food) so max rating is at heap top; ties broken by lexicographically smaller food
            heapq.heappush(self.cuisine_to_heap[c], (-r, f))

    def changeRating(self, food, newRating):
        # Update current rating map and push new entry into cuisine heap (lazy deletion)
        cuisine = self.food_to_cuisine[food]
        self.food_to_rating[food] = newRating
        heapq.heappush(self.cuisine_to_heap[cuisine], (-newRating, food))

    def highestRated(self, cuisine):
        heap = self.cuisine_to_heap[cuisine]
        # Pop stale entries until the heap top matches current rating
        while heap:
            neg_rating, food = heap[0]
            current_rating = self.food_to_rating.get(food)
            # If current_rating matches -neg_rating, this is valid
            if current_rating is not None and -neg_rating == current_rating:
                return food
            # Otherwise stale entry; remove it
            heapq.heappop(heap)
        # By problem constraints, cuisine always has at least one food, so we shouldn't get here.
        return ""
```
- Notes:
  - The heap stores tuples (-rating, food). Negative rating makes Python's min-heap behave like a max-heap by rating. For equal ratings, tuple ordering uses the food string, so the lexicographically smaller food will be chosen automatically.
  - changeRating does not remove the old tuple from the heap immediately (lazy deletion). It pushes the updated tuple; stale tuples are removed later when highestRated examines the heap top.
  - Time complexity:
    - Initialization: O(n log n) for pushing n items.
    - changeRating: O(log n) for pushing onto a heap for that cuisine.
    - highestRated: Amortized O(log n). A single call may pop multiple stale entries, but each stale entry was produced by a prior rating change (or initial insert) and is popped at most once across all calls.
  - Space complexity: O(n + u) where u is the number of updates (total heap entries across all heaps), bounded by O(n + number_of_calls).