# [Problem 1717: Maximum Score From Removing Substrings](https://leetcode.com/problems/maximum-score-from-removing-substrings/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)

- the substrings are overlapping, so removing instances of one can potentially reduce the number of instances of the other you can remove.
- It might not always be better to remove all instances of whichever is worth more points first, if removing one instance of the substring worth more points "messes up" more than one instance of the substring worth fewer points, and the former is worth <2x the latter.
  - I think this scenario is possible... e.g., say `"ab"` is worth 2 points, `"ba"` is worth 3 points, and the string is `"abab"`.
- ah, important insight from example 1 -- instances of the substrings can be created from letters that were initially non-adjacent when we remove substrings between them. So given `"aabb"`, we can get points for 2 `"ab"`s by removing the middle 2 characters first. So this means my example above no longer applies... and in that case I think it *is* always best to remove instances of the highest-value substring first...
  - I can't come up with any sequences of letters where removing the higher-value substring first would break two instances of the lower-value substring without creating another instance of one or the other for us to get points from. And if the scenario I was thinking of requires one substring's value to be <2x the other's, then one of each will always be worth more than two of the less valuable one.
- But we can't just remove all instances of the higher-value substring, then all instances of the lower-value substring, and then say we're done, because removing either type could create new instances of the same type or the other type. So I think we'll need multiple passes through...
- I could use `re.subn()` to remove all (currently existing) instanes of a given substring at once and also get the number of replacements made, which I'll need in order to know what to add to the total score. `.replace()` would be simpler and probably faster but I wouldn't know how many instances were removed. And since the string can be very long, slicing via indices to remove them one at a time could be super slow
  - oh, duh... that's unnecessary -- since both substrings are 2 characters, I can just use `.replace()`, subtract the length of the string after from its length before, and divide by 2.
- okay, I *will* need at least 2 passes through (1 for each substring) but I think I could avoid needing multiple passes through *per* substring if I keep track of the most recent character in something like a stack... if I just used `.replace()` to remove all instances of the higher-value substring at once, I'd need to check whether doing so created more instances of that same substring before moving onto the lower-value substring, and continue doing so until it didn't (realistically, this shouldn't happen *too* many times, but I could see one of the test cases being a contrived example where it does). But if I iterate through characters and keep track of whether the most recent character (top of the stack) is the first character of the higher-value substring, then I can catch instances where removing the next 2 characters causes that most recent character becomes part of a new substring instance
  - in fact, I'd need to track more than the most recent character in case this happened multiple times. Though I'd only really need to keep track of as many most-recent characters as there were consecutive instances of the higher-value substring's starting character
  - this seems more complicated, so I'm gonna start with the multiple-pass, `str.remove()` approach first

## Refining the problem, round 2 thoughts

- So my [**first attempt**](#first-attempt) took too long when removing one (or more) instance(s) of a substring repeatedly created (a) new instance(s) of it. So now I'm gonna try the "single pass per substring" I mentioned above. I'll iterate through the string, identify substrings along the way, and keep track of the most recent characters before that in a stack so that if I remove a substring, then the next character I encounter can be used to make a second instance of that substring with the character preceding the just-removed substring, I can catch that on the same iteration.
- I think I'll need to do this separately for each of the two substring types, which means I'll actually have to modify the string while dealing with the higher-value substring so that when I then go to deal with the lower-value substring, I only consider the remaining/not-already-used characters.
- strings can't be modified in place in Python, so I'll need to create the post-higher-value-substring-removal string as I go. I can think of two ways to do this:
  - as I iterate through the initial string, push all characters (that I don't remove) onto the stack, then I can just `''.join()` the stack at the end.
  - convert the initial string to a list, iterate over it, remove items used in higher-value substrings as I encounter them, and then `''.join()` the remaining items in the list back to a string at the end.
    - I think this version would be more memory-efficient -- instead of building up a big stack that contains the entire post-higher-value-substring-removal string, I would only need to use it to track the most recent characters that are the first character in the higher-value substring, and I could clear the stack entirely whenever I encounter a character other than that.
    - But I also think it'd be slower, because I'd have to `.pop(0)` items from the front of the initial-string-converted-to-a-list as I go, which is **way** slower (in Python) than `.pop()`ping from the end of a list.
      - though I could use `collections.deque` instead of a list, which doesn't have this issue.
    - Modifying the list as I iterate over would also be tricky -- I'd have to use a `while` loop and increment the current index, which would be potentially confusing (but not impossible) to keep track of because at various points I might pop 2 items off the front (initial string contains the higher-value substring) or 1 item off the front (initial string contains the 2nd character of the higher-value substring, and top of the stack is the 1st character)
      - actually no, this isn't how it'd work -- since I'd be removing items that are part of higher-value-substring instances in this version, I'd only need to increment the index by 1 if the current character couldn't be used to make an instance of it.
  - I could spend all day weighing these, I'm just gonna go with the first for now
- since I'll need to do this once for each of the two substring types, and the logic means the body of the loop is going to be fairly long, I'm gonna abstract this to its own helper function
- ah, also, I'm going to initialize the stack with a "dummy" character that isn't in either substring of interest so that I can always check `stack[-1]` without having to also check whether the stack contains any items in order to avoid an `IndexError`
  - similarly, I'm going to pad the string with a dummy character on the end so I can check `s[<current_index> + 1]` for the 2nd substring character without worrying about `IndexError`s

## Attempted solution(s)

### First attempt

```python
class Solution:
    def maximumGain(self, s: str, x: int, y: int) -> int:
        total_points = 0
        if x > y:
            first_substring = "ab"
            second_substring = "ba"
            first_points = x
            second_points = y
        else:
            first_substring = "ba"
            second_substring = "ab"
            first_points = y
            second_points = x

        while True:
            if first_substring in s:
                len_before = len(s)
                s = s.replace(first_substring, "")
                total_points += (len_before - len(s)) / 2 * first_points
            elif second_substring in s:
                len_before = len(s)
                s = s.replace(second_substring, "")
                total_points += (len_before - len(s)) / 2 * second_points
            else:
                return int(total_points)
```

> realistically, this shouldn't happen *too* many times, but I could see one of the test cases being a contrived example where it does

yep, called it 🙃 time limit exceeded on test case 65/76, where `s = `... I'm not pasting that whole thing in but it's equivalent to the output of `f"{'a'*25_000}{'b'*50_000}{'a'*25_000}"`. So I guess it's time to figure out the stack-based approach. GOTO [**Refining the problem, round 2 thoughts**](#refining-the-problem-round-2-thoughts).

### Second attempt

```python
class Solution:
    def maximumGain(self, s: str, x: int, y: int) -> int:
        if x > y:
            first_substring = "ab"
            second_substring = "ba"
            first_points = x
            second_points = y
        else:
            first_substring = "ba"
            second_substring = "ab"
            first_points = y
            second_points = x

        initial_len = len(s)
        s = self._remove_substring(s, first_substring)
        len_after_first = len(s)
        s = self._remove_substring(s, second_substring)
        len_after_second = len(s)

        return (initial_len - len_after_first) // 2 * first_points + (len_after_first - len_after_second) // 2 * second_points

    def _remove_substring(self, full_str, substr):
        full_str += '.'
        stack = ['.']
        substr_char1, substr_char2 = substr
        ix = 0
        n_iters = len(full_str) - 1

        while ix < n_iters:
            curr_char = full_str[ix]
            if curr_char == substr_char1 and full_str[ix+1] == substr_char2:
                ix += 2
            elif curr_char == substr_char2 and stack[-1] == substr_char1:
                stack.pop()
                ix += 1
            else:
                stack.append(curr_char)
                ix += 1

        return ''.join(stack[1:])
```

![](https://github.com/user-attachments/assets/161eeec1-54ab-48c0-bd72-d074c4d59780)

still kinda slow, but I'm short on time and need to move on, so I'm satisfied with it for now.
