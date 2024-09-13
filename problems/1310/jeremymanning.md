# [Problem 1310: XOR Queries of a Subarray](https://leetcode.com/problems/xor-queries-of-a-subarray/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- There might be an "efficient" way to do this, but I'm just going to compute this manually
- For each query (`[left, right]`), we can loop through from `left` to `right`, taking the XOR of the result plus the next element each time
- Once we reach `right`, we can append the result to the `answer` list

## Refining the problem, round 2 thoughts
- I think this is straightforward...the potential catch is that we might run out of time
- Maybe there's a way to re-use computations...but let's try the easy version first

## Attempted solution(s)
```python
class Solution:
    def xorQueries(self, arr: List[int], queries: List[List[int]]) -> List[int]:
        answers = []
        for left, right in queries:
            x = arr[left]
            for i in range(left + 1, right + 1):
                x ^= arr[i]
            answers.append(x)
        return answers
```
- Given test cases pass
- Let's try submitting

![Screenshot 2024-09-13 at 3 42 14 PM](https://github.com/user-attachments/assets/6fdca782-a782-47ec-9501-d03202fbfbc0)

Hrmph, time limit exceeded.  Bummer.

## More brainstorming
- Sadly I think we'll need to do something more efficient that enables us to re-use computations
- Let's see...the way to do this is usually to think about fundamental properties of the main operation/function, and see if anything can be exploited.  What do we know about XORs?
    - We know XOR is associative-- e.g., A XOR (B XOR C) is the same as (A XOR B) XOR C
    - We know XOR of A with itself is 0
    - We know XOR of A with 0 is A
    - So...
- Maybe we can compute the "cumulative XOR" up to each index, `i`
- Then the query answer would just be XOR(right) XOR XOR(left - 1) -- i.e., the XOR of everything up to `right`, but then XORing out everything before `left`
- We can compute the initial cumulative pass through in $O(n)$ time (where $n$ is the length of `arr`)
- The time to compute every query is constant (just a single XOR operation), so the total time is $O(n + q)$ where $n$ is the length of the array and $q$ is the number of queries.  But really this is just $O(max(n, q))$.
- Anyways...let's try it!
```python
class Solution:
    def xorQueries(self, arr: List[int], queries: List[List[int]]) -> List[int]:
        cumulative_xor = [0] * (len(arr) + 1)
        for i in range(1, len(arr) + 1):
            cumulative_xor[i] = cumulative_xor[i - 1] ^ arr[i - 1]

        answers = []
        for left, right in queries:
            answers.append(cumulative_xor[right + 1] ^ cumulative_xor[left])

        return answers
```
- Given test cases (still) pass
- Submitting...

![Screenshot 2024-09-13 at 3 53 49 PM](https://github.com/user-attachments/assets/7204f56c-02ce-4f46-9156-bff544da656b)

Solved!
