# [Problem 1395: Count Number of Teams](https://leetcode.com/problems/count-number-of-teams/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)

- This is... different. The approach here isn't immediately obvious to me...
- Maybe I could construct some sort of tree or graph where each item in the array ("soldier") is a node with directed edges to all other items in the array that come after it. Then I could traverse the tree/graph starting from each item in the array (up to the 3rd from last, I think) and count the number of 3-node paths I'm able to follow where each node's value is either less than or more than the previous node's.
  - Would this actually be any faster than the naïve approach though? Or have I just complicated the problem for no reason? The naïve approach would be something like:
    ```python
    n_teams = 0
    for ix1, solider1 in enumerate(rating[:-2]):
        for ix2, soldier2 in enumerate(rating[ix1+1:-1]):
            for soldier3 in rating[ix1+ix2+2:]:
                if soldier1 < soldier2 < soldier3 or soldier1 > soldier2 > soldier3:
                    n_teams += 1
    ```
    and there's no way that's going to be tractable.
  - maybe instead of starting at every node and stopping after 3 items, I could go all the way to the bottom of the tree and get out longer sequences of increasing/decreasing values? Then given a sequence of $n$ increasing/decreasing values, the number of 3-node paths it contains would be $\frac{n \times (n - 1) \times (n - 2)}{6}$.
    - I think it'd be hard to avoid double-counting subsequences with this approach though... e.g., if I'm given `[7, 6, 999, 5, 4, 998, 3, 2, 997, 1]`, I'd first DFS (or something like that) from `7`, and... yeah never mind I don't think this is going to work.
    - The combinations idea feels worth exploring further though...
- Another idea : what if I created two $n \times n$ binary matricies: a "`less_than_matrix`" and a "`greater_than_matrix`". In the `less_than_matrix`, `less_than_matrix[i][j]` will be 1 if `rating[j] < rating[i]` and 0 if it's greater, and in the `greater_than_matrix`, `greater_than_matrix[i][j]` will be 1 if `rating[j] > rating[i]` and 0 if it's less (I think I'd only use the upper triangle of each matrix, so maybe I could somehow combine them to save space)? Then:
  - for each matrix row `i` (item in the `rating` array):
    - for each matrix column `j` (where `j > i` to restrict it to the upper triangle; i.e., subsequent items in the `rating` array):
      - if `less_than_matrix[i][j]` is 1, then the sum of `less_than_matrix[j]` gives me the number of soldiers that could be the 3rd person on a "decreasing" team with soldiers `i` and `j`.
      - if `greater_than_matrix[i][j]` is 1 (which it will be if `less_than_matrix[i][j]` is 0), then the sum of `greater_than_matrix[j]` gives me the number of soldiers that could be the 3rd person on an "increasing" team with soldiers `i` and `j`.
        - I could slice off just `*_matrix[j][i:]`, since all the values before column `i` would be 0, but I think that would take more time than it'd save.
  - I think this would be $O(n^2)$ time and space complexity, which still seems like it's not ideal, but it's at least faster than the naïve approach, which would be $O(n^3)$ time.
    - actually... I'm pretty sure `sum()` takes $O(n)$ time, so this might still be $O(n^3)$ 😕 let's at least try it though since it's pretty straightforward to implement.

## Refining the problem, round 2 thoughts

## Attempted solution(s)

```python
class Solution:
    def numTeams(self, rating: List[int]) -> int:
        len_rating = len(rating)
        less_matrix = [[0] * len_rating for _ in range(len_rating)]
        greater_matrix = [[0] * len_rating for _ in range(len_rating)]

        for i in range(len_rating):
            for j in range(i + 1, len_rating):
                if rating[j] < rating[i]:
                    less_matrix[i][j] = 1
                else:
                    greater_matrix[i][j] = 1

        n_teams = 0
        for i in range(len_rating):
            for j in range(i + 1, len_rating):
                if less_matrix[i][j]:
                    n_teams += sum(less_matrix[j])
                elif greater_matrix[i][j]:
                    n_teams += sum(greater_matrix[j])

        return n_teams
```

![](https://github.com/user-attachments/assets/4dd1c88e-e064-4f34-beba-871799bde1cf)

Yep, I was afraid of that 😕 But I have another idea I thought of while writing that one out that I think is worth trying...
- the "increasing" and "decreasing" teams have a sort of "complimentary symmetry" (not sure what to call this) in that they consist of a middle soldier, 1 soldier whose rating is greater than theirs, and 1 soldier whose rating is less than theirs. The only difference is that for the "decreasing" team, the "greater" soldier has to come before them in the array and the "lesser" soldier has to come after them in the array, and vice versa for the "increasing" team.
- Since all values in `rating` are unique, all soldiers before and after a given "middle soldier" will be either greater or less than them. And a given middle soldier can form a valid "increasing" team with any preceding lesser soldier and any subsequent greater soldier -- and vice versa for "decreasing" teams. So the total number of teams a given middle soldier can form is `n_preceding_lesser_soldiers * n_subsequent_greater_soldiers + n_preceding_greater_soldiers * n_subsequent_lesser_soldiers`.
- So I think I could actually solve this in approximately $O(n^2)$ time if I:
  - treat each soldier between `rating[1]` and `rating[-2]` as the "middle" soldier in a team
  - loop over the soldiers before them in the list and count the number of "lesser" and "greater" soldiers
  - loop over the soldiers after them in the list and do the same thing
  - multiply the corresponding counts together and add them to a running total
  - repeat for each soldier in `rating[1:-1]`
- I'll try this next

```python
class Solution:
    def numTeams(self, rating: List[int]) -> int:
        n_teams = 0
        for middle_ix, middle_soldier in enumerate(rating[1:-1], start=1):
            n_before_less = n_before_greater = 0
            for soldier in rating[:middle_ix]:
                if soldier < middle_soldier:
                    n_before_less += 1
                else:
                    n_before_greater += 1
            for soldier in rating[middle_ix+1:]:
                if soldier < middle_soldier:
                    n_teams += n_before_greater
                else:
                    n_teams += n_before_less
        return n_teams
```

![](https://github.com/user-attachments/assets/42513e69-4f96-472e-875a-b0bceb68ab0f)

Nice, that turned out to be way simpler than anything I was thinking of in the beginning.
