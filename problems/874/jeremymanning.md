# [Problem 874: Walking Robot Simulation](https://leetcode.com/problems/walking-robot-simulation/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- I'm thinking we'll want to keep track of the current position and heading
- The position could be represented as two numbers `(x, y)`
- The heading could be represented as two numbers also:
    - North: `(0, 1)`
    - East: `(1, 0)`
    - South: `(0, -1)`
    - West: `(-1, 0)`
- So the full position would be: `[(x, y), (a, b)]`
- We'll also need to keep track of the "order" of turning:
    - Clockwise/right: north --> east --> south --> west
    - Counterclockwise/left: north --> west --> south --> east
- To move forward `i` units (assuming no obstables), we can update the new position to `[(x + i * a, y + i * b), (a, b)]`
- If there are obstacles, things could get messy-- every time we move (but not when we turn), we'll need to check if we've hit *any* obstacle
    - I'm not sure how to get away from having to do this...
    - We'll need to check if the *next* move will result in a collision (and if so, we don't make that move)
    - This also, I think tells us what to do with the "there can be an obstacle in [0, 0]" note-- I initially thought it might cause the robot to get stuck at `(0, 0)`.  But actually, maybe we can just treat that like any other obstacle.  Note: we'll need to check this special case when testing, because the instructions are a little ambiguous.
- Finally, the squared distance is easy to compute-- it's just `x ** 2 + y ** 2`, since we always start at the origin.  Any time we move, we'll need to compare the current distance with the current max (intialized to 0).  Then at th eend we just return `max_distance`.

## Refining the problem, round 2 thoughts
- We should initialize `position = [(0, 0), (0, 1)]`.  Or actually, we could just represent the position as `[x, y, a, b]` instead of using nested lists-- so let's intialize `position = [0, 0, 0, 1]`
- Turning left (`next_command == -2`) and right (`next_command == -1`):
```python
def turn_left(pos):
    x, y, a, b = pos
    if a == 0:  # currently either north or south
        if b == 1:  # north
            a, b = -1, 0
        else:       # south
            a, b = 1, 0
    else:       # currently either east or west
        if a == 1:  # east
            a, b = 0, 1
        else:       # west
            a, b = 0, -1
    return x, y, a, b

def turn_right(pos):
    x, y, a, b = pos
    if a == 0:  # currently either north or south
        if b == 1:  # north
            a, b = 1, 0
        else:       # south
            a, b = -1, 0
    else:       # currently either east or west
        if a == 1:  # east
            a, b = 0, -1
        else:       # west
            a, b = 0, 1
    return x, y, a, b
```
- To walk forward, we have to both check for obstacles (one step ahead) and update `max_distance` each time `x` or `y` changes.
- First, let's see how we'll check for obstacles:
```python
def collision(x, y):
    for xo, yo in obstacles:
        if x == xo and y == yo:
            return True
    return False
```
- Then we can move as follows (if `next_command >= 1`):
```python
def move(pos, steps, max_distance):
    x, y, a, b = pos
    for _ in range(steps):
        x_next, y_next = x + a, y + b
        if collision(x_next, y_next):
            break        
        x, y = x_next, y_next
        max_distance = max(max_distance, x ** 2 + y ** 2)
    return (x, y, a, b), max_distance
```
- I think this is everything...let's put it together!

## Attempted solution(s)
```python
class Solution:
    def robotSim(self, commands: List[int], obstacles: List[List[int]]) -> int:
        max_distance = 0
        pos = [0, 0, 0, 1]

        def turn_left(pos):
            x, y, a, b = pos
            if a == 0:  # currently either north or south
                if b == 1:  # north
                    a, b = -1, 0
                else:       # south
                    a, b = 1, 0
            else:       # currently either east or west
                if a == 1:  # east
                    a, b = 0, 1
                else:       # west
                    a, b = 0, -1
            return x, y, a, b
        
        def turn_right(pos):
            x, y, a, b = pos
            if a == 0:  # currently either north or south
                if b == 1:  # north
                    a, b = 1, 0
                else:       # south
                    a, b = -1, 0
            else:       # currently either east or west
                if a == 1:  # east
                    a, b = 0, -1
                else:       # west
                    a, b = 0, 1
            return x, y, a, b

        def collision(x, y):
            for xo, yo in obstacles:
                if x == xo and y == yo:
                    return True
            return False

        def move(pos, steps, max_distance):
            x, y, a, b = pos
            for _ in range(steps):
                x_next, y_next = x + a, y + b
                if collision(x_next, y_next):
                    break        
                x, y = x_next, y_next
                max_distance = max(max_distance, x ** 2 + y ** 2)
            return (x, y, a, b), max_distance

        for c in commands:
            if c == -2:
                pos = turn_left(pos)
            elif c == -1:
                pos = turn_right(pos)
            else:
                pos, max_distance = move(pos, c, max_distance)

        return max_distance
```
- Given test cases pass
- Let's try a case where there's an obstacle at 0,0:
    - `commands = [5, 6, 7, 2, 7, -1, -2, 5, 6, -2, 3, 5, 7, 9, 1, 1, -1, 2, 3, 4, -2, 5], obstacles = [[0, 0], [5, 2], [-3, -6]]`: pass
- Ok...so I'm pretty sure the algorithm is right.  I'm not totally certain that it's efficient enough (so we might time out)...but let's try submitting...

![Screenshot 2024-09-03 at 11 29 06 PM](https://github.com/user-attachments/assets/0165408c-0186-479e-96b3-39204daeb8d3)

Hrmph, I was afraid that would happen 😞...

- One potentially simple fix would be to convert `obstacles` to a `set` instead of a `list`: `obstacles = {(x, y) for x, y in obstacles}`
- Then lookups will be constant time instead of $O(n)$ time for $n$ obstacles-- so we could just use:
```python
class Solution:
    def robotSim(self, commands: List[int], obstacles: List[List[int]]) -> int:
        max_distance = 0
        obstacles = {(x, y) for x, y in obstacles}
        pos = [0, 0, 0, 1]

        def turn_left(pos):
            x, y, a, b = pos
            if a == 0:  # currently either north or south
                if b == 1:  # north
                    a, b = -1, 0
                else:       # south
                    a, b = 1, 0
            else:       # currently either east or west
                if a == 1:  # east
                    a, b = 0, 1
                else:       # west
                    a, b = 0, -1
            return x, y, a, b
        
        def turn_right(pos):
            x, y, a, b = pos
            if a == 0:  # currently either north or south
                if b == 1:  # north
                    a, b = 1, 0
                else:       # south
                    a, b = -1, 0
            else:       # currently either east or west
                if a == 1:  # east
                    a, b = 0, -1
                else:       # west
                    a, b = 0, 1
            return x, y, a, b

        def collision(x, y):
            return (x, y) in obstacles

        def move(pos, steps, max_distance):
            x, y, a, b = pos
            for _ in range(steps):
                x_next, y_next = x + a, y + b
                if collision(x_next, y_next):
                    break        
                x, y = x_next, y_next
                max_distance = max(max_distance, x ** 2 + y ** 2)
            return (x, y, a, b), max_distance

        for c in commands:
            if c == -2:
                pos = turn_left(pos)
            elif c == -1:
                pos = turn_right(pos)
            else:
                pos, max_distance = move(pos, c, max_distance)

        return max_distance
```
- Test cases still pass; let's see if that pushes us far enough over the threshold...

![Screenshot 2024-09-03 at 11 34 34 PM](https://github.com/user-attachments/assets/55255ae3-6087-4a35-b9e7-186cb2ebbb74)

Great, solved!

