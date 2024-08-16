# [Problem 624: Maximum Distance in Arrays](https://leetcode.com/problems/maximum-distance-in-arrays/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- Since the arrays are sorted, we know that only the first and last elements in each array matter
- The brute force solution would be:
    - Compute the minimums and maximums of each array: `bounds = [[a[0], a[-1]] for a in arrays]`
    - For each minimum, compute the maximum (from the other arrays) that's farthest away
    - This requires $O(m^2)$ time (for the $m$ arrays), which is likely intractable since $m$ could be as large as $10^5$.
- Another possibility would be to tackle this in a dynamic programming way.  What if we keep track of the *two* largest and smallest values, along with the array indices they come from?
    - The smallest minimum + the largest maximum from any other array.  If a new minimum is found, we can now potentially update the largest maximum if it happened to be from the same array as the previous smallest minimum.
    - The largest maximum + the smallest minimum from any other array.  If a new maximum is found, we can now potentially update the smallest minimum if it happened to be from the same array as the previous largest maximum.

## Refining the problem, round 2 thoughts
- Some things to work out:
    - How do we track the *two* smallest minima or the two largest maxima?  We could initialize them to the first two minima/maxima (from the first two arrays).  Then if we find a smaller minimum or a larger maximum in a future array, we can either replace the second smallest/largest or add the new values to the front and remove the second smallest/largest.
    - If the "next" array in the sequence has *both* a larger maximum *and* a smaller minimum, then we can only update *either* the maxima or the minima.  We should choose whichever results in the larger absolute difference.
    - This makes me realize that we probably only need to keep track of the *single* smallest minimum and the *single* largest maximum, since if we just consider each array in turn it's not possible for a previous max/min to have come from the new array we're considering.
    - We just need to initialize the max and min using the first two arrays (based on what yields the largest absolute difference)
    - Then for each successive array, `a`:
        - If `a[0] < current_min and a[-1] > current_max`:
            - If abs(a[0] - current_max) > abs(current_min - a[-1]):
                - `current_min = a[0]`
            - Else:
                - `current_max = a[-1]`
        - Else:
            - If `a[0] < current_min`, `current_min = a[0]`
            - If `a[-1] > current_max`, `current_max = a[-1]`
    - Then we just return `abs(current_max - current_min)`
- One potential edge case: what if we're in that first condition (where the new array, `i`, has *both* the new minimum and maximum values).  We only get to replace the current min *or* max.  Suppose we replace the min, since that results in a larger difference.  But later on in the sequence, for some further-along array `j`, suppose we find an even *smaller* minimum (i.e., `j[0] < i[0]`), but no array after `i` has a larger value than `i[-1]`.  Now we've missed out on a larger absolute difference, since we chose the wrong replacement of the `current_min` and `current_max` when we got to array `i`.  So actually, we probably *do* need to keep track of those sorts of discarded options:
    - We could initialize `discarded_min = float('inf')` and `discarded_max = float('-inf')`.  Then we could update the logic of the first case above as follows:
        - for each successive array, `a`:
            - If `a[0] < current_min and a[-1] > current_max`:
                - If abs(a[0] - current_max) > abs(current_min - a[-1]):
                    - `current_min = a[0]`
                    - `discarded_max = a[-1]`
                - Else:
                    - `current_max = a[-1]`
                    - `discarded_min = a[0]`
            - Else:
                - If `a[0] <= current_min`:
                    - `current_min = a[0]`
                    - If `discarded_max > current_max`:
                        - `current_max = discarded_max`
                - If `a[-1] >= current_max`:
                    - `current_max = a[-1]`
                    - If `discarded_min < current_min`:
                        - `current_min = discarded_min`
        - Now return `abs(current_max - current_min)`
- Ok...I'm not 100% confident in this approach, but let's try it...
 
## Attempted solution(s)
```python
class Solution:
    def maxDistance(self, arrays: List[List[int]]) -> int:
        discarded_min, discarded_max = float('inf'), float('-inf')
        if abs(arrays[0][0] - arrays[1][-1]) > abs(arrays[0][-1] - arrays[1][0]):
            current_min, current_max = arrays[0][0], arrays[1][-1]
        else:
            current_min, current_max = arrays[1][0], arrays[0][-1]
            if abs(arrays[0][0] - arrays[1][-1]) == abs(arrays[0][-1] - arrays[1][0]):
                discarded_min, discarded_max = arrays[0][0], arrays[1][-1]

        for a in arrays[2:]:
            if a[0] < current_min and a[-1] > current_max:
                if abs(a[0] - current_max) > abs(current_min - a[-1]):
                    current_min = a[0]
                    discarded_max = a[-1]
                else:
                    current_max = a[-1]
                    discarded_min = a[0]
            else:
                if a[0] <= current_min:
                    current_min = a[0]
                    if discarded_max > current_max:
                        current_max = discarded_max
                if a[-1] >= current_max:
                    current_max = a[-1]
                    if discarded_min < current_min:
                        current_min = discarded_min

        return abs(current_max - current_min)
```
- Given test cases pass
- Let's generate some random new arrays:
    - `arrays = [[-88, -37, -32, -24, -5], [-59, 49, 53], [-31, 18, 34, 52, 59], [-7, 74], [-92, 4], [-31, 23], [-86, -12, 63, 67], [-66, -48, -12, 89], [-57, -16, -10, -5], [-91, -60, 65, 77, 85], [-61, -18, 53], [-50, -22], [-41, -32, 28, 47, 90], [-34, -11, 1, 35, 47], [-3, 11, 93, 95], [-19], [-63, -32, 7], [56]]`: pass
    - `arrays = [[-57, -27], [-92], [-86, 66], [-50, -21, -4, 23], [-96, 55, 63, 88], [-66, 81], [-94, -79, 4, 35], [91, 96], [-30, -3, 14, 55, 66], [56], [-5], [-95, -61, 50, 63], [-23, 29, 35], [-55, 87], [-99, -48, 34, 71, 97], [-97, -49, 52, 53], [-84, -41, 19, 28], [-78]]`: pass
    - `arrays = [[-51, -5, 16, 72, 89], [-94, -68, 13], [-100, -73], [-80, -48, -17, -7, 47], [-17, 51], [-88, -6]]`: pass
- Ok...let's submit!

![Screenshot 2024-08-15 at 11 18 37 PM](https://github.com/user-attachments/assets/f76a11c8-7a27-4846-9030-5fdac59b0cbb)

Bummer...it fails for `arrays = [[1,3],[-10,-9,2,2,3,4],[-8,-5,2],[-10,-6,-5,-5,0,3],[-8,-6,-2,0,2,3,3],[-10,-10,-5,0]]`.  I can see that for this one there are three arrays where the minimum is -10.  The max across all arrays is 4, but that includes one of those -10 arrays.  What I was hoping would happen is:
    - Given the first two arrays, intialize: `current_min, current_max, discarded_min, discarded_max = -10, 3, float(`-inf`), 4`
    - But I'm seeing that this actually isn't what the start of my code does...let's see if we can patch it up a bit.
```python
class Solution:
    def maxDistance(self, arrays: List[List[int]]) -> int:
        discarded_min, discarded_max = float('inf'), float('-inf')
        if abs(arrays[0][0] - arrays[1][-1]) > abs(arrays[0][-1] - arrays[1][0]):
            current_min, current_max = arrays[0][0], arrays[1][-1]
            if arrays[1][0] < current_min:
                dicarded_min = arrays[1][0]
            if arrays[0][-1] > current_max:
                discarded_max = arrays[0][-1]
        else:
            current_min, current_max = arrays[1][0], arrays[0][-1]
            if arrays[0][0] < current_min:
                dicarded_min = arrays[0][0]
            if arrays[1][-1] > current_max:
                discarded_max = arrays[1][-1]

        for a in arrays[2:]:
            if a[0] < current_min and a[-1] > current_max:
                if abs(a[0] - current_max) > abs(current_min - a[-1]):
                    current_min = a[0]
                    discarded_max = a[-1]
                else:
                    current_max = a[-1]
                    discarded_min = a[0]
            else:
                if a[0] <= current_min:
                    current_min = a[0]
                    if discarded_max > current_max:
                        current_max = discarded_max
                if a[-1] >= current_max:
                    current_max = a[-1]
                    if discarded_min < current_min:
                        current_min = discarded_min

        return abs(current_max - current_min)
```
- Ok, that fixes that test case
- But...now a new case is failing (`arrays = [[-10,-9,-9,-3,-1,-1,0],[-5],[4],[-8],[-9,-6,-5,-4,-2,2,3],[-3,-3,-2,-1,0]]`):

![Screenshot 2024-08-15 at 11 27 01 PM](https://github.com/user-attachments/assets/af2ff6e8-e5ea-4608-bbc0-a947ada9db0b)


- I can see a few things:
    - There are a bunch of single-element arrays, so that might be messing with the logic I've used:
        - Do I ever need to ensure that the same single element isn't used as *both* the min and max?  I don't think so, since we're only selecting at most one element from a given array anyway.
        - But maybe the initial logic where I set `discarded_min` and `discarded_max` is still faulty?  I think this may be a problem-- I forgot to account for the case where `abs(arrays[0][0] - arrays[1][-1]) == abs(arrays[0][-1] - arrays[1][0])`.  If so, then...what do we do?
- Actually maybe there's an even simpler solution:
    - initialize `current_min, current_max, max_dist = arrays[0][0], arrays[0][-1], 0`
    - Now loop through the remaining arrays:
        - Replace `max_dist` with `max(max_dist, abs(a[-1] - current_min), abs(a[0] - current_max))`
        - Replace `current_min` with `min(current_min, a[0])`
        - Replace `current_max` with `max(current_max, a[-1])`
    - Then just return `max_dist`
    - Now we don't need to deal with these edge cases.
- Let's try it...
     
```python
class Solution:
    def maxDistance(self, arrays: List[List[int]]) -> int:
        current_min, current_max, max_dist = arrays[0][0], arrays[0][-1], 0
        for a in arrays[1:]:
            max_dist = max(max_dist, abs(a[-1] - current_min), abs(a[0] - current_max))
            current_min = min(current_min, a[0])
            current_max = max(current_max, a[-1])
        return max_dist
```
- Now the previously failing test cases pass
- Let's try a few more:
    - `arrays = [[79], [-59, 35], [-58, 81], [-100, -73, 17, 58], [-66, -31, -9, -2], [20, 37, 39], [-93, -43, -6, 27, 53], [-30], [-59, -18, 8, 59], [-68, -67, -31, -13, 66], [-65, -50, 99], [-70, -56, 41, 70], [-96, -90, 56], [-79, 23, 39, 78], [-77, -52, 45]]`: pass
    - `arrays = [[-20, 1, 25, 88, 94], [-53, -47, 88], [-84, -30, -19, 16, 95], [-27, 4, 46, 79], [-87, -79, -47, -23, 43], [-66, -51, 31, 85], [-20], [-54, 29], [-100, 1, 51, 98], [-89, -84, 15], [49], [-95, 18], [-83, -80, -25, 83, 91], [-25, 52], [-30], [-71, -8, 81, 92, 100]]`: pass
- Ok...let's submit again...

![Screenshot 2024-08-15 at 11 40 57 PM](https://github.com/user-attachments/assets/cffeb74d-cbc0-44a2-be05-504570150a5c)

Solved!

Some post-mortem reflections on this one:
- I was a bit too eager to finish this quickly, which resulted in submitting too early before I had fully thought through the logic or potential edge cases.  Ironically this resulted in the full thing taking *longer* than I think it could have otherwise.
- I sort of used the given test cases to "debug," but this seems akin to "overfitting" (maybe not *quite* cheating outright, but feels close!)
- It turns out this was a pretty simply problem after I took a step back and stopped over-thinking it.  Good to keep in mind for the future!
