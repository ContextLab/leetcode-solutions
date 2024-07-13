# [Problem 2751: Robot Collisions](https://leetcode.com/problems/robot-collisions/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)

- all robots are moving at the same speed, so any moving in same direction can't collide
  - if all characters in `directions` are the same, can just return `healths`
- also, any moving away from each other won't collide
  - after filtering for same direction, can filter remaining opposite-direction movers for instances where one moving `R` has a larger `directions` value than another moving `L`.
- this feels complex enough that I think it might be worth writing a `Robot` class to track attributes for each robot
- order in which collisions happens will be important, because removed robot then won't collide with subsequent ones it would've otherwise encountered
  - maybe this means I'll want to simulate this in terms "timesteps" so I can make sure to execute collision logic in the right order
  - though simulation solutions are rarely the most optimal, and it seems like leetcode usually includes a test case that'd cause simulation-based solutions to time out
  - I think the scenario where a simulation would be bad is if the colloding robots start very far from each other, causing me to have to simulate a bunch of noop timesteps (and check whether any robots are in the same location for each of them) before something actually happens. But I think I can avoid this by -- at each timestep where a collision happens, as well as the first -- finding the minimum distance between collision-eligible pair of robots and immediately advancing time by that many steps.
- instead of simulating individual timesteps, could I figure this out from the initial positions and direction of the robots?
  - I think so, if I start with the rightmost robot moving right and collide it with further-right robots that're moving left until it's dead... at which point I could move onto the next-rightmost right-moving robot and collide it with further-right left-moving robots
  - Would this work with a scenario like example 3, where there are two indepenedent, simultaneous collisions?
    - collide robot 3 with robot 4
      - if it survives, we know it'll be in the returned array and we can move onto robot 1
      - if it dies, we also move onto robot 1
    - in either case, next move onto robot 1, collide it with robot 2
      - if it survives
        - if robot 4 survived the robot 3 vs 4 collision
          - collide robot 1 with robot 4
          - the survivor will be in the returned array
        - if robot 3 survived the robot 3 vs 4 collision
          - robot 1 will be in the returned array
      - if it dies, robot 2 *and* robot 4 will be in the returned array
  - I *think* this will work... I think I'll just need 2 separate lists(?) to keep track of right-moving and left-moving robots independently, so I can figure out which to collide with which
    - also, both will need to be sorted so I can access the "next" robot from each list correctly
    - I'd need to loop over robots to construct those two list anyway... if I pre-sort the initial list of robots moving in both directions, can I just do the collisions at the same time?
    - this feels like it's trying to get me to use a stack... or two?
  - let's say I get the list of robots in position order (I'll figure out how later). Then I could:
    - create a stack for right-moving robots (and one for left-moving robots?)
    - for each robot
      - if it's moving right, push it onto a stack of right-moving robots
        - this means the stack will also be in order of position, with the rightmost right-moving robot on top... yeah this definitely feels like how they're trying to get me to solve it... I think
      - else (it's moving left), check whether there are any right-moving robots on the stack
        - if there aren't, we know that robot is a survivor, and can move onto the next robot in the list
        - else (there are) collide it with the right-moving robot on top of the stack
          - if the left-moving robot survives, pop the right-moving robot off the stack (can discard because we know it didn't survive) and collide the left-moving robot with the new top-most right-moving robot, and so on
            - (I think this means I'll actually need to use a `while` loop for checking whether there are robots in the stack instead of `if`/`else`)
          - else (the right-moving robot survived) move onto the next robot in the sorted list and repeat
          - ah, also need to account for equal health -- neither survives in that case
    - any robots on the stack when we get to the end of the list are survivors
    - also, seems like I *won't* need a separate stack for left-moving robots
- how do i get the survivor list back into the right order?
  - if I create a bunch of `Robot` objects, I could initialize them with an attr for their original index, and then sort the survivor list by `key=lambda robot: robot.<that_attr>`
    - but the constraints say there can be up to $10^5$ robots, so creating that many objects -- even small, optimized ones with `namedtuple` or `dataclass` -- would take a ton of memory and also initialization time...
    - what value do I keep track of in the stack of right-moving robots if I'm not using `Robot` objects though?
  - could I create some sort of mapping between the robots' pre- and post-sorting indices?
  - `np.argsort` would be nice here... alas
    - could I create the equivalent output some other way?
    - I could create a list of indices, and then sort that according to `positions` without *actually* sorting positions... then instead of sorting `positions` in the first place and mapping thos indices onto `healths`, `directions` , then trying to map backwards, I could use the sorted list of indices to get the next index from all 3 input lists for the current iteration.
      - ooo important note with this though -- I wouldn't want to actually remove any defeated robots from any of the lists while iterating, because that would mess up the mapping. Also, once I determine the "current" robot is a survivor, I can't just append them to the list I'll eventually return because I'm iterating in sorted order and not input order.
        - *But* all the input lists are still in their original order, including `healths`, which is the basis for the values I need to return... so I could just modify `healths` in-place and return that at the end.
          - I'd have to filter 0's to remove defeated robots before returning it... which ultimately means another loop, so this might just be a wash. But it's the idea I have right now so I'll go with it...

## Refining the problem, round 2 thoughts

- I'll add a "short-circuit" condition where we check whether all robots are moving in the same direction, and if so, return `healths` immediately
- There's another possible circumstance where we could short-circuit early -- if all robots moving leftward start out to the left of all robots that're moving rightward. But I'm not sure this is really worth implementing because we'd need to check this against a sorted `position` list, which would require at least an additional loop to run for all test cases, and would probably end up taking more time overall since I'm willing to bet this scenario appears once, if at all. So I'll forego this.

## Attempted solution(s)

```python
class Solution:
    def survivedRobotsHealths(self, positions: List[int], healths: List[int], directions: str) -> List[int]:
        if all(d == directions[0] for d in directions):
            return healths

        sorted_ixs = list(range(len(positions)))
        sorted_ixs.sort(key=lambda i: positions[i])
        right_movers_stack = []

        for curr_ix in sorted_ixs:
            if directions[curr_ix] == 'R':
                right_movers_stack.append(curr_ix)
            else:
                while len(right_movers_stack) > 0:
                    rightmost_right_mover_ix = right_movers_stack[-1]
                    rightmost_right_mover_health = healths[rightmost_right_mover_ix]
                    if rightmost_right_mover_health > healths[curr_ix]:
                        healths[curr_ix] = 0
                        healths[rightmost_right_mover_ix] -= 1
                        break
                    elif rightmost_right_mover_health == healths[curr_ix]:
                        healths[curr_ix] = 0
                        healths[rightmost_right_mover_ix] = 0
                        right_movers_stack.pop()
                        break
                    else:
                        right_movers_stack.pop()
                        healths[rightmost_right_mover_ix] = 0
                        healths[curr_ix] -= 1

        return list(filter(None, healths))
```

![](https://github.com/user-attachments/assets/8a60614f-f696-4922-8308-887508c6f70c)

yay!
