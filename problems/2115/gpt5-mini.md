# [Problem 2115: Find All Possible Recipes from Given Supplies](https://leetcode.com/problems/find-all-possible-recipes-from-given-supplies/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to find which recipes can be made given initial supplies and that recipes can be ingredients for other recipes. This looks like a dependency problem: a recipe requires some ingredients, some of which might be other recipes. If all required ingredients are either in supplies or can be produced, the recipe is producible.

Topological sort (Kahn's algorithm) comes to mind: treat each recipe as a node; when a recipe becomes available, it can satisfy dependencies for other recipes. Count how many required ingredients of each recipe are not currently available; when that count reaches zero we can produce it. Ingredients that are neither in supplies nor in recipes make a recipe impossible (no one will ever decrement that requirement).

Alternatively, DFS with cycle detection and memoization works too, but BFS/topological is straightforward and efficient.

## Refining the problem, round 2 thoughts
Refinements and edge cases:
- Build a mapping recipe -> index to efficiently reference nodes.
- For each recipe, compute indegree = number of ingredients not initially in supplies. For ingredients that are recipes, create a directed edge from that ingredient-recipe node to the current recipe node so when the ingredient recipe is produced we can decrement indegree.
- If an ingredient is neither in supplies nor in the recipes set, the indegree will include it and there will be no incoming edge to ever decrement it — that's correct (the recipe cannot be produced).
- Cycles between recipes are naturally handled: their indegrees never reach zero so they are not produced.
- Complexity: building graph O(sum of lengths of ingredients lists), BFS also linear in nodes + edges. Space O(n + edges).

I'll implement Kahn's algorithm: initialize queue with recipes whose indegree == 0 (all ingredients already in supplies). Pop, add to result, for each dependent recipe decrement indegree and enqueue if it becomes 0.

## Attempted solution(s)
```python
from collections import deque, defaultdict
from typing import List

class Solution:
    def findAllRecipes(self, recipes: List[str], ingredients: List[List[str]], supplies: List[str]) -> List[str]:
        n = len(recipes)
        recipe_index = {r: i for i, r in enumerate(recipes)}
        supply_set = set(supplies)

        indegree = [0] * n
        adj = defaultdict(list)  # edge from recipe idx (ingredient) -> list of recipe idx that depend on it

        # Build indegree and adjacency
        for i, ingr_list in enumerate(ingredients):
            cnt = 0
            for ing in ingr_list:
                if ing in supply_set:
                    # already available, no need to wait
                    continue
                if ing in recipe_index:
                    # dependency on another recipe
                    indegree[i] += 1
                    adj[recipe_index[ing]].append(i)
                else:
                    # ingredient neither in supplies nor a recipe -> impossible to satisfy
                    indegree[i] += 1

        # Start with recipes that have zero unmet ingredients
        q = deque()
        for i in range(n):
            if indegree[i] == 0:
                q.append(i)

        result = []
        while q:
            cur = q.popleft()
            recipe_name = recipes[cur]
            result.append(recipe_name)
            # producing this recipe can satisfy other recipes that depend on it
            for nei in adj[cur]:
                indegree[nei] -= 1
                if indegree[nei] == 0:
                    q.append(nei)

        return result
```
- Notes about approach:
  - This is a topological-sort / Kahn's algorithm approach on the dependency graph where edges go from an ingredient recipe to the recipes that depend on it.
  - indegree[i] counts how many required ingredients for recipes[i] are not currently available. Ingredients in supplies don't increase indegree. Ingredients that are other recipes add an edge so when that recipe is produced we decrement indegree. Ingredients that are neither in supplies nor recipes increase indegree but have no incoming edge to ever decrement it, which correctly prevents the recipe from being produced.
  - Time complexity: O(R + E) where R = number of recipes and E = total number of ingredient entries (sum of lengths of all ingredients lists). Building maps and adjacency takes O(E). BFS processes each edge and node at most once.
  - Space complexity: O(R + E) for the adjacency list, indegree array, and maps.