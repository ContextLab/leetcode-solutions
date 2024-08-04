# [Problem 1508: Range Sum of Sorted Subarray Sums](https://leetcode.com/problems/range-sum-of-sorted-subarray-sums/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- The "naive" solution would be:
    - Make the set of subarray sums (this takes $O(n^2)$ time and space, where $n$ is the length of the array)
    - Sort the sums (this takes $O(n^2 \log n^2)$ time)
    - Return the sum of the relevant range
- I think the naive solution will be too slow
- I'm wondering if sorting `nums` at the start will be useful:
    - We know that the sets with the smallest sums will contain lower-valued elements
    - I feel like there "should" be a way of generating the subsets' sums in order.  For example, after sorting:
        - The smallest subset will be just the first element
        - The second smallest subset will contain the second number
        - The third subset will contain either:
            - The third number alone OR
            - The first and second numbers (if their sum is smaller than the third number)
        - The fourth subset will contain either:
            - The fourth number alone OR
            - The first and second numbers (if their sum is larger than the third number but smaller than the fourth) OR
            - The first, second, and third numbers (if their sum is smaller than the fourth) OR
            - The first and third numbers OR
            - The second and third numbers
        - And so on.  In general, the $k^{\mathrm{th}}$ subset will be one of the $\frac{k * (k + 1)}{2}$ subsets comprised of numbers from in the sorted array at (1-indexed) positions from $1...k$.  Hmm.
        - Could we enumerate these options systematically?  E.g.:
            - Start looking for subsets of length 1
            - Prioritizing subsets of length 1, check whether any length 2 subset is smaller
                - This requires also checking whether any length 3 subset is smaller, and so on... 🤔
            - Maybe we could look in sliding windows?
                - Start of sliding window: position `i` (initialize to 0)
                - Intialize `width = 1`
                - Initialize `j = i + width`  (note: I'm thinking of something like taking `sorted_nums[i:j]`...but it's not going to work when `width > 2`...still, let's see if we can get this idea down before refining it...)
                - While `sorted_nums[i + 1] < sum(sorted_nums[i:j])` and `j < len(nums)`:  (note: this isn't quite right, but the idea is to do something like "while the next length $k$ subset is still greater than length $k + 1$ subsets, keep checking length $k + 1$ subsets until they're exhausted.  Then move on to $k + 2$ subsets, and so on.  Once we exceed the next length $k$ subset's sum, we can stop enumerating and add the next length $k$ subset to the list.
                    - I'm thinking we should probably do this in a queue 🤔...
- How might enumerating subsets in a queue work?
    - Let's start by enqueing every item in the sorted list (`sorted_nums`), along with its position
    - To generate the next subset, we might do something like:
        - Pop the first subset in the queue (`q1`).  Let's call it `x1`.
        - Start a new queue (`q2`) where we explore adding each possible remaining item (after the last element of the popped subset, `x1`) to the popped subset
        - Now, while `q2` isn't empty:
            - Pop the first element in `q2`.  Let's call it `x2`.
            - If the sum for `x2` is greater than for the (new) first subset in `q1`, break (note: and...somehow enque...the item before `x2`?  Something....in `q1`...?)
            - Otherwise enque (in `q2`) new subsets comprising `x2` plus each possible element in `sorted_nums` that comes after the last item's position in `x2`.
    - This isn't quite right...but maybe on the right track?
    - Let's put this aside for the moment.  Let's assume we have a to-be-written function that will give us the "next" subset in the sequence.  And...somehow it's written in an efficient way.  Maybe as a generator?
        - The "simple" approach would be to generate `left - 1` subsets using this function
            - Then once we get to the `left`th subset, we start aggregating the sums, until we get to the `right`th subset.  Then we return the aggregated sum.
        - A more efficient approach, if it were possible, would be to "jump ahead" somehow.  E.g., this would be possible if we could somehow know in advance what the `left`th subset was, without enumerating the previous subsets, and then start our aggregation process there.
            - One thing I can think of is that we *could* do this jumping ahead if we knew that all length $k$ subsets had smaller sums than any length $k + 1$ subsets.  If we wanted to skip ahead to index `i`, then we know that the first $n$ subsets are of length 1, the next $n - 1$ subsets are of length 2, the next $n - 2$ subsets are of length 3, and so on.
            - So the number of subsets with length less than or equal to $k$ is:
                - $(n + 0) + (n + 1) + (n + 2) + ... + (n + k - 1)$.  There are $k$ "$n$s" in this sequence, plus the numbers $0 ... k - 1$.  So if we add those up we get...
                - $kn + $ the sum of the numbers from 0 to $k - 1$, which is $\frac{k^2 - k}{2}$... so in summary, there are $kn + \frac{k^2 - k}{2}$ subsets of (up to) length $k$.
                - This means that, to figure out where index $i$ is in the sequence, we could just figure out the value of $k$ for which the number of subsets of up to length $k$ is greater than $i$, but the number of subsets of length $k - 1$ is *less* than $i$.  Then the $i^\mathrm{th}$ subset can be found by skipping over the first $i - (k - 1)n + \frac{(k - 1)^2 - k + 1}{2}$ subsets of length less than or equal to $k$ (which will include some number of subsets of length $k$ at the end).  I'm not sure that this will help us...but... 🤷

## Refining the problem, round 2 thoughts
- I think I'm stuck.  So what I'm going to try is:
    - I'll implement the "naive" solution that I outlined above
    - I'll test it to make sure it works on the given test problems and some other made-up examples
    - I'll submit it
    - If the code times out, I'll need to refine the approach and think of something more efficient
 
## Attempted solution(s)
```python
class Solution:
    def rangeSum(self, nums: List[int], n: int, left: int, right: int) -> int:
        mod = 10**9 + 7

        sums = []
        for i in range(n):
            x = 0
            for j in range(i, n):
                x += nums[j]
                sums.append(x)

        sums.sort()
        return sum(sums[left - 1:right]) % mod
```
- Given test cases pass
- New test cases (let's make up some long ones using random numbers):
    - `n = 1000, nums = [38, 3, 55, 33, 42, 36, 97, 2, 87, 82, 8, 27, 78, 26, 82, 38, 90, 10, 63, 42, 91, 81, 88, 91, 68, 95, 8, 43, 43, 76, 31, 62, 45, 79, 86, 46, 45, 75, 72, 40, 11, 62, 75, 48, 77, 1, 13, 19, 56, 67, 43, 14, 64, 34, 63, 40, 59, 100, 100, 15, 68, 42, 1, 81, 61, 49, 80, 44, 31, 59, 72, 12, 44, 18, 21, 32, 44, 40, 32, 49, 9, 62, 53, 95, 18, 24, 13, 73, 88, 6, 9, 52, 9, 60, 30, 69, 12, 36, 100, 37, 7, 58, 75, 22, 27, 20, 47, 74, 86, 67, 79, 100, 66, 23, 6, 8, 8, 25, 13, 53, 7, 50, 46, 94, 98, 57, 43, 44, 25, 82, 30, 90, 49, 85, 50, 90, 3, 31, 84, 50, 13, 49, 44, 27, 6, 41, 95, 29, 51, 15, 68, 56, 50, 51, 37, 51, 87, 71, 71, 35, 25, 43, 43, 77, 77, 35, 14, 15, 85, 57, 10, 53, 97, 4, 33, 52, 69, 38, 91, 47, 63, 42, 11, 44, 8, 5, 85, 79, 31, 55, 76, 2, 9, 59, 30, 42, 4, 53, 95, 90, 10, 44, 98, 18, 38, 72, 40, 47, 50, 52, 49, 36, 86, 23, 78, 25, 33, 88, 3, 28, 26, 75, 91, 10, 56, 75, 61, 27, 75, 69, 9, 85, 39, 32, 36, 67, 80, 80, 91, 60, 56, 38, 2, 40, 94, 72, 61, 68, 10, 9, 51, 27, 66, 56, 27, 45, 93, 67, 17, 20, 52, 53, 24, 57, 10, 75, 7, 24, 60, 20, 83, 26, 25, 69, 83, 23, 11, 91, 39, 65, 74, 89, 46, 78, 15, 12, 18, 58, 97, 11, 55, 78, 65, 26, 39, 93, 59, 20, 60, 52, 37, 90, 44, 92, 92, 96, 59, 41, 72, 96, 12, 86, 62, 57, 96, 28, 84, 86, 8, 67, 14, 36, 7, 34, 68, 50, 90, 68, 68, 20, 74, 39, 82, 2, 4, 43, 87, 21, 69, 84, 60, 56, 80, 16, 94, 23, 71, 92, 69, 24, 95, 3, 36, 42, 92, 70, 71, 28, 90, 42, 66, 2, 71, 8, 61, 15, 6, 16, 7, 69, 13, 19, 36, 97, 45, 100, 99, 48, 90, 37, 42, 55, 88, 7, 67, 41, 63, 64, 56, 91, 7, 23, 45, 54, 68, 31, 38, 61, 29, 60, 100, 53, 86, 72, 92, 6, 97, 43, 63, 19, 45, 6, 48, 1, 90, 93, 44, 14, 48, 2, 73, 93, 74, 93, 93, 10, 50, 83, 100, 54, 50, 63, 13, 32, 88, 1, 46, 18, 14, 56, 17, 13, 9, 17, 54, 73, 40, 92, 27, 19, 78, 66, 30, 9, 5, 17, 13, 73, 15, 74, 84, 17, 19, 37, 70, 73, 57, 100, 18, 95, 44, 76, 27, 82, 22, 58, 47, 88, 13, 51, 38, 94, 93, 29, 76, 87, 30, 54, 39, 88, 78, 48, 53, 8, 9, 21, 57, 5, 47, 49, 64, 93, 49, 77, 7, 60, 67, 76, 60, 70, 22, 56, 31, 31, 8, 19, 97, 79, 79, 10, 8, 37, 75, 79, 28, 10, 57, 25, 22, 71, 95, 50, 48, 72, 4, 34, 41, 45, 3, 94, 12, 48, 84, 49, 6, 8, 90, 26, 55, 88, 61, 17, 48, 28, 68, 62, 96, 100, 71, 66, 96, 80, 52, 84, 66, 50, 33, 2, 43, 14, 50, 79, 42, 2, 16, 90, 37, 15, 31, 28, 31, 84, 61, 38, 15, 99, 91, 91, 67, 53, 78, 59, 50, 71, 83, 52, 76, 36, 96, 5, 8, 9, 46, 95, 52, 49, 96, 79, 54, 24, 68, 55, 67, 10, 83, 16, 28, 60, 89, 33, 1, 56, 81, 47, 97, 65, 59, 38, 92, 41, 21, 43, 96, 70, 15, 7, 79, 19, 98, 40, 7, 61, 12, 19, 63, 69, 29, 13, 58, 73, 15, 92, 60, 77, 81, 20, 52, 86, 9, 83, 22, 25, 18, 94, 16, 76, 28, 66, 30, 52, 33, 36, 13, 79, 80, 92, 82, 62, 30, 10, 36, 99, 90, 39, 37, 32, 54, 38, 69, 49, 83, 99, 67, 99, 97, 41, 55, 27, 8, 62, 96, 32, 20, 77, 14, 65, 84, 5, 61, 15, 28, 14, 12, 13, 51, 95, 41, 45, 30, 95, 22, 19, 35, 73, 56, 63, 9, 35, 39, 98, 6, 83, 23, 13, 48, 71, 78, 39, 23, 39, 44, 43, 26, 69, 94, 66, 53, 77, 75, 25, 77, 73, 23, 30, 38, 46, 3, 12, 97, 23, 97, 50, 58, 80, 33, 30, 24, 96, 39, 3, 61, 68, 14, 7, 96, 91, 89, 67, 5, 65, 90, 62, 96, 82, 14, 5, 1, 12, 61, 14, 88, 89, 32, 65, 99, 26, 83, 71, 32, 21, 21, 99, 91, 59, 85, 67, 59, 23, 19, 95, 40, 19, 48, 100, 81, 64, 53, 30, 62, 23, 47, 14, 47, 24, 8, 12, 63, 63, 99, 5, 14, 16, 40, 84, 99, 57, 5, 91, 35, 80, 34, 67, 44, 20, 91, 2, 78, 99, 1, 30, 52, 13, 55, 48, 8, 78, 9, 87, 29, 3, 78, 3, 54, 81, 42, 35, 43, 97, 92, 43, 55, 54, 70, 7, 63, 61, 80, 80, 80, 30, 52, 39, 30, 61, 84, 34, 72, 75, 27, 15, 27, 72, 19, 39, 90, 56, 2, 46, 22, 12, 53, 33, 25, 95, 10, 12, 57, 95, 44, 10, 25, 24, 18, 19, 56, 17, 60, 35, 8, 16, 77, 78, 77, 47, 4, 47, 56, 46, 32, 29, 51, 30, 9, 35, 11, 7, 73, 87, 83, 78, 90, 65, 100, 32, 17, 46, 7, 16, 11, 35, 99, 86, 100, 78, 31, 46, 20, 42, 21, 89, 24, 80, 66, 55, 20, 87, 50, 79, 40, 71, 21, 74, 47, 59, 64, 9, 49, 77, 31, 85, 53, 56, 57, 46, 85, 34, 11, 3, 15, 21, 12, 5, 92, 93, 55, 54, 61, 53, 16, 84], left = 100, right = 500`: passes...
    - `n = 1000, nums = [81, 45, 8, 99, 86, 48, 76, 90, 80, 27, 8, 45, 1, 86, 31, 39, 64, 89, 98, 34, 24, 63, 89, 52, 3, 23, 51, 79, 22, 84, 26, 42, 95, 87, 20, 95, 4, 71, 74, 32, 56, 74, 44, 46, 23, 11, 73, 11, 66, 66, 21, 37, 14, 78, 82, 56, 93, 93, 16, 65, 23, 58, 67, 2, 62, 17, 26, 79, 10, 78, 83, 17, 76, 59, 17, 73, 51, 39, 87, 66, 50, 33, 18, 45, 32, 69, 52, 1, 83, 60, 10, 9, 38, 47, 15, 66, 19, 14, 86, 44, 12, 6, 79, 70, 25, 14, 96, 27, 94, 99, 100, 4, 68, 15, 53, 10, 58, 89, 21, 90, 2, 33, 30, 84, 87, 64, 35, 32, 96, 32, 96, 24, 92, 87, 1, 55, 30, 38, 9, 6, 21, 65, 79, 29, 46, 64, 11, 23, 15, 41, 24, 3, 98, 51, 58, 65, 6, 72, 32, 54, 19, 9, 65, 99, 84, 24, 44, 94, 6, 71, 26, 7, 77, 67, 99, 57, 21, 70, 56, 81, 57, 19, 35, 19, 90, 27, 39, 29, 92, 90, 77, 99, 53, 84, 91, 28, 5, 97, 10, 93, 37, 3, 32, 30, 59, 30, 20, 42, 15, 5, 5, 4, 6, 73, 38, 29, 54, 23, 92, 41, 82, 27, 7, 41, 71, 45, 53, 2, 45, 90, 25, 34, 57, 13, 18, 82, 99, 40, 4, 84, 83, 11, 24, 97, 25, 20, 19, 87, 48, 10, 70, 51, 51, 52, 66, 36, 23, 94, 2, 41, 50, 2, 16, 73, 95, 34, 45, 21, 70, 68, 42, 31, 96, 45, 55, 33, 67, 38, 3, 78, 100, 43, 10, 42, 78, 59, 99, 56, 88, 54, 53, 63, 5, 82, 1, 62, 84, 91, 99, 72, 50, 43, 16, 88, 22, 55, 29, 35, 10, 47, 49, 45, 40, 91, 66, 5, 85, 26, 55, 7, 5, 53, 79, 71, 3, 77, 86, 68, 91, 86, 11, 66, 59, 76, 8, 83, 9, 44, 27, 44, 45, 56, 38, 14, 13, 11, 40, 48, 13, 89, 87, 97, 97, 7, 87, 90, 45, 78, 61, 91, 94, 16, 42, 32, 19, 4, 43, 87, 18, 64, 65, 45, 19, 7, 70, 71, 67, 77, 80, 14, 13, 7, 43, 99, 58, 55, 85, 33, 85, 40, 75, 76, 30, 49, 24, 11, 1, 43, 49, 30, 7, 35, 80, 83, 30, 94, 49, 41, 43, 92, 33, 6, 38, 80, 97, 22, 84, 65, 93, 2, 20, 48, 88, 69, 88, 98, 68, 42, 42, 56, 31, 54, 1, 73, 41, 75, 78, 20, 79, 12, 42, 60, 33, 59, 66, 21, 25, 88, 72, 66, 32, 83, 65, 43, 34, 22, 50, 86, 80, 44, 20, 59, 61, 25, 1, 87, 59, 87, 50, 95, 85, 78, 82, 46, 78, 2, 90, 47, 61, 75, 5, 41, 33, 39, 25, 3, 74, 1, 2, 20, 93, 53, 54, 72, 77, 72, 66, 11, 4, 39, 70, 30, 37, 66, 84, 35, 37, 55, 32, 87, 79, 17, 93, 59, 23, 81, 5, 65, 6, 82, 97, 33, 44, 39, 87, 90, 32, 5, 46, 76, 51, 79, 85, 62, 40, 48, 74, 95, 30, 9, 13, 59, 65, 9, 13, 44, 3, 16, 78, 93, 67, 76, 32, 18, 83, 93, 24, 68, 56, 77, 8, 50, 64, 79, 92, 9, 55, 62, 97, 81, 76, 100, 2, 79, 11, 50, 21, 24, 9, 28, 97, 58, 3, 9, 83, 92, 54, 87, 78, 55, 97, 17, 26, 81, 98, 59, 33, 4, 93, 55, 27, 33, 22, 80, 75, 85, 19, 50, 71, 19, 49, 86, 55, 59, 48, 66, 84, 19, 21, 65, 71, 54, 100, 47, 54, 47, 44, 3, 38, 59, 65, 53, 75, 57, 46, 89, 11, 76, 7, 100, 50, 6, 28, 7, 53, 24, 23, 56, 40, 98, 31, 41, 4, 9, 57, 97, 57, 76, 100, 15, 93, 81, 88, 18, 11, 42, 89, 63, 31, 31, 34, 9, 54, 100, 24, 77, 76, 7, 35, 73, 11, 76, 82, 67, 67, 72, 22, 3, 75, 84, 41, 4, 56, 66, 14, 28, 99, 85, 2, 73, 30, 60, 30, 25, 77, 78, 32, 42, 77, 36, 96, 39, 75, 67, 62, 30, 90, 74, 80, 73, 98, 85, 17, 66, 41, 19, 97, 40, 1, 14, 47, 18, 52, 55, 81, 26, 61, 2, 25, 96, 5, 60, 3, 90, 39, 76, 58, 14, 89, 43, 87, 34, 58, 96, 4, 81, 41, 56, 26, 77, 76, 22, 81, 55, 67, 53, 72, 29, 32, 69, 96, 79, 90, 29, 8, 35, 49, 77, 40, 8, 13, 5, 70, 40, 43, 66, 76, 35, 87, 79, 14, 37, 100, 67, 86, 44, 7, 64, 44, 10, 93, 39, 60, 4, 4, 11, 5, 3, 47, 28, 62, 25, 12, 53, 33, 88, 42, 76, 42, 85, 98, 9, 58, 92, 58, 87, 91, 13, 31, 48, 66, 70, 79, 3, 79, 38, 13, 27, 34, 86, 9, 49, 59, 57, 55, 3, 89, 2, 85, 30, 65, 27, 36, 60, 72, 95, 6, 8, 31, 26, 32, 96, 86, 17, 15, 59, 96, 10, 86, 13, 42, 88, 94, 97, 2, 97, 75, 65, 83, 86, 2, 78, 43, 34, 100, 42, 2, 6, 37, 89, 90, 43, 47, 64, 21, 22, 60, 91, 3, 84, 56, 29, 48, 90, 69, 42, 32, 56, 47, 61, 39, 22, 74, 1, 48, 22, 99, 62, 47, 31, 74, 34, 51, 2, 88, 66, 22, 62, 20, 23, 26, 84, 38, 20, 7, 40, 4, 39, 26, 24, 17, 34, 33, 55, 40, 48, 64, 53, 56, 77, 46, 1, 9, 38, 80, 73, 19, 38, 100, 15, 29, 98, 24, 68, 2, 52, 68, 62, 99, 7, 65, 23, 46, 8, 59, 6, 94, 29, 6, 81, 60, 91, 67, 73, 5, 72, 65, 75, 7, 6, 27, 96, 41, 63, 85, 85, 58, 33, 51, 8], left = 1000, right = 50000`: pass
    - Submitting... 🤞

![Screenshot 2024-08-04 at 12 09 36 AM](https://github.com/user-attachments/assets/71ac581e-3b00-42ea-97c4-ef2a102bbe79)

Ok!

 
