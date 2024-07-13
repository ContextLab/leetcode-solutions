# [Problem 2751: Robot Collisions](https://leetcode.com/problems/robot-collisions/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- Oooh, our first "hard" rated problem so far!  And with robots! 🤖➡️ ⬅️🤖
- Ok, so I'm seeing two potential ways to solve this off the top of my head:
    - Running out the full simulation and keeping track of everything.  This would work for small-scale versions of the problem, but it'd be terribly inefficient.  In each timestep we need to keep track of potential collisions between every pair of robots.  So the runtime would be something like $O(dn^2)$, where $d$ is the max position ($10^9$) and $n$ is the number of robots, which could be up to $10^5$.  Clearly this isn't going to scale.
    - Some sort of heap-based solution.  What makes me think of heaps is that we know the positions come in unsorted, so we need some way of "sorting" the robots.  Also, robots moving left will only colide with robots moving right (and vice versa).  For robots moving left, anything to the left of the leftmost right-moving robot will remain unchanged (never collide).  Similarly, any right-moving robot to the right of the rightmost left-moving robot will remain unchanged.  The collisions happen between...what?  Let's see...
        - We know that right-moving robots will never collide with each other, and left-moving robots will never collide with each other
        - So we only have to compare positions *between* right- and left-moving robots
        - Well...hmm
- Suppose that the robot positions *were* sorted.  (We could sort them in $O(n \log n)$ time if needed...)
    - We could do something using a stack, looping through each robot in turn:
        - If the stack is empty, push the next robot and continue
        - Otherwise, we want to do something like the following, looping until either the stack is empty or the robot crashes:
            - Check the top of the stack
                - If the robot there is moving in the same direction, or if the robots are moving in opposite directions but have already passed each other, pop the top of the stack (and...probably put that robot in...another stack?) and then break
                - If the robots are going to crash (opposite drections and haven't passed each other yet):
                    - If the top-of-stack robot has more health, remove the current robot and break.  Probably update the position of the top-of-stack robot (to the current robot's position?  to some mid point between the two robots' positions? hmm...)
                    - If the current robot has more health, pop the top of the stack (and delete that robot), decrement the current robot's health by 1, possibly update the current robot's position (in some way we still need to figure out), and then continue
        - Then at the end, re-sort the remaining robots and return their health values.  We could represent each robot as a vector, `x`, where `x[0]` is the robot's position, `x[1]` is the robot's direction, and `x[2]` is the robot's health.  I'm not sure yet if we'll need to track it, but it might be useful to also have `x[3]` be the time step for that robot (e.g., the number of positions moved from its starting position).  That time step property could (maybe?) come in handy if we had to account for updates that occurred out of order...although at the moment I'm not sure that would actually be possible.
- Since the inputs *aren't* sorted, I was thinking we might want to have one heap (a max heap?) for robots moving to the right, indexed by position.  The other heap (a min heap?) would be for left-moving robots, again indexed by position.  Then we could do something like:
    - If the left-most left moving robot...eh...I'm having trouble thinking this through.  Could we compare its position with the top of the right-moving robot heap?
- Hmm...  Maybe let's take a step back.  Ideas so far that seem promising:
    - I still think the full simulation will be too inefficient, so let's nix that idea officially
    - I can't think of how the heap idea would actually work, so let's nix that too
    - I think the stack idea is promising.  Now how do we actually implement it... 🤔
    - I also think we're going to need to sort the positions.
    - I like the "robots as a vector" idea.  Robots could also be represented as dicts.  Probably lists/vectors require less memory?
- Ok, so let's go back to assuming the robot positions are now sorted, and each robot is a vector.  How might this stack idea work...
    - Let's go through each robot in turn.  We know we're starting with the left-most robot and moving right along the track:
        - If the robot is moving _right_, it's not going to collide with anything pushed on the stack so far (because everything will be to its left and moving at the same speed), so let's push it to the stack and continue.
        - If the robot is moving _left_, then it might crash into anything moving right that's in the stack.  Let's check the top of the stack:
            - If that top robot is *also* moving left, then we can push our new robot to the top of the stack (they're not going to collide)
            - While whatever robot is on top is moving _right_, then they're going to crash: the top-of-stack robot (`a`) is to the left of the new robot (`b`) and moving right, and `b` is to the right of `a` and moving left.  So:
                - if `a.health > b.health` then `b` disappears and we should decrement `a.health` by 1.  Note: can health go negative?  If it does, what happens?
                - If `a.health < b.health` then we should pop `a`, decrement `b.health` by 1 (again, potential negative health issue!), and continue checking for the next top-of-stack robot
                - If `a.health == b.health` then pop `a` and break (i.e., `b` gets deleted)
                - If the stack is every empty, or if the top robot is moving left, then push `b` to the top of the stack
- I think this could work; let's go with it...

## Refining the problem, round 2 thoughts
- A few issues to sort out still:
    - Can health ever go negative?  And if so, what happens?
        - Suppose two robots, `a` and `b`, are about to collide.  If they have never collided with another robot, then their health values are at least 1.
        - If both have health of 1, then they both disappear.
        - If only 1 has a health of 1, it dies and the other robot survives (since its health must be bigger than 1)
        - In the *next* collision, whatever robot it collides with *also* must have a health of at least 1 (since it has *also* either never collided, or survived with at least 1 health before that point).
        - So actually, health can never be negative
    - With the stack idea, I think we can figure out which robots survive and what their final health values are.  However, they may not end up in the same orders they started in, since the positions could be out of sorted order.  So I think we need to track each robots position in the _sequence_ as well as its position along the track.  In the last step (before we return the answer) we'll need to sort by sequence position.  That will take $O(n \log n)$ time, but that's fine since we've already paid that cost with our initial sort.
    - I'm still somewhat concerned about runtime.  Suppose we have something like R R R R ... R R R R L L L ... L L L L.  All of those R-moving robots get pushed on the stack.  But now, for each L robot, of which there are $O(n)$ we're going to need to test *every* R robot, of which there are _also_ $O(n)$.  So this might be an $O(n^2)$ algorithm, which could be too slow.  In practice we won't actually quite hit $n^2$ steps, since robots will be eliminated (and therefore either it's and R robot and won't need to be re-checked, or it's an L robot and won't need to be checked against the remaining R robots) as we progress.
        - At the moment I'm not sure how to improve on this...so again, let's maybe just go with it and see what happens...

## Attempted solution(s)
```python
class Solution:
    def survivedRobotsHealths(self, positions: List[int], healths: List[int], directions: str) -> List[int]:
        bots = sorted(zip(positions, directions, healths, range(len(positions))), key=lambda x: x[0])

        stack = []
        for pos, dir, health, i in bots:
            if len(stack) == 0 or dir == 'R':
                stack.append([pos, dir, health, i])
            else:  # dir == 'L'
                while health > 0 and len(stack) > 0 and stack[-1][1] == 'R':  # collision...
                    if health > stack[-1][2]:   # new robot survives, old dies
                        health -= 1
                        stack.pop()
                    elif health < stack[-1][2]: # new robot dies, old survives
                        stack[-1][2] -= 1
                        health = 0
                    else:                       # both die
                        health = 0
                        stack.pop()                    

                if health > 0:
                    stack.append([pos, dir, health, i])

        return [x[2] for x in sorted(stack, key=lambda x: x[3])]
```
- Given test cases: pass
- I'm almost out of time for the night, so I'm just going to make up a some totally random test cases in the hopes that if I'm missing an edge case it'll show up there:
    - `positions, healths, directions = [67, 234, 51, 7, 45678, 2, 65, 46, 90, 101, 21, 44, 45, 6, 1], [1, 788, 54, 6, 3, 3, 456, 765, 234, 1, 700, 876, 34, 54, 94], "RLRRLRRLLRLLLRL"`: pass(!!)
    - `positions, healths, directions = [67, 234, 51, 7, 45678, 2, 65, 46, 90, 101, 21, 44, 45, 6, 1], [1, 788, 54, 6, 3, 3, 456, 765, 234, 1, 700, 876, 34, 54, 94], "RLLLRRLLRLLLRRL"`: pass
- Ok...I'll just submit this; I can't think of any obvious remaining edge cases.  My main concern is that the runtime is still bad, but I also can't think of an obvious faster solution 🙃.

![Screenshot 2024-07-12 at 11 40 17 PM](https://github.com/user-attachments/assets/39d3287d-3a27-4fde-9ba4-63ff79ecd0f4)

Well alrighty then!  I'll call that done!

