# [Problem 2807: Insert Greatest Common Divisors in Linked List](https://leetcode.com/problems/insert-greatest-common-divisors-in-linked-list/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- Woohoo, _another_ linked list problem 🥳!  Maybe this is linked list month?
- There are two pieces to this problem:
    - First, computing greatest common divisors.  This is easy-- we can just use the built-in `math.gcd` function.
        - Note: there's probably a faster way to compute the GCD when the "factors" are repeated.  E.g., if we have a list `a --> b --> c` then we end up computing `b`'s factors for `math.gcd(a, b)` *and* `math.gcd(b, c)`.  We could optimize the process by just computing the factors once, and then storing them in a hash table for the next time they're reused.  This would increase the memory requirement, but would improve the time.  Nevertheless, I'm going to stick with `math.gcd` (despite this inefficiency); I'm choosing simplicity of the implementation over "optimality," given the constraints of the problem (we're not dealing with any _super_ long lists, for example).
    - Second, inserting new nodes.  To do that we need to:
        - Create a new `ListNode`
        - Set its value of the greatest common divisor of the previous/next nodes
        - Set it's `next` attribute to `previous.next`
        - Set the `previous.next` to the new node

## Refining the problem, round 2 thoughts
- The only "tricky" (?) part is keeping track of the "previous" node.  But that's just a bookkeeping thing.
- Let's put everything together

## Attempted solution(s)
```python
import math

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def insertGreatestCommonDivisors(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = head
        node = head.next
        while node is not None:
            gcd = math.gcd(prev.val, node.val)
            x = ListNode(val=gcd, next=node)
            prev.next = x

            prev = node
            node = node.next
        return head
```
- Given test cases pass
- I can't think of any useful edge cases beyond what's already in the given examples (e.g., just having a single node), so let's submit!

![Screenshot 2024-09-09 at 10 20 05 PM](https://github.com/user-attachments/assets/0759659e-9cbf-45ff-ae30-377700e139d4)

Solved!
