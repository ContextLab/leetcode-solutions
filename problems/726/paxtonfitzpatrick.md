# [Problem 726: Number of Atoms](https://leetcode.com/problems/number-of-atoms/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)

- Hmmm... this one is labeled "hard", but it doesn't seem that bad, unless I'm missing something...
- ah, the tricky part is going to be dealing with nested parentheses. But still, I don't think that will be too hard.
- Okay, it seems like there will be some general things we'll need to deal with, and also some special cases I'll want to consider how to handle.

### General stuff

- I'll iterate through the `formula` string, and use a `collections.Counter` to keep track of the counts of each atom. Let's call this `elem_counts`.
- I'll want to build up the name of the element currently being parsed, so I'll initialize an empty string, something like `curr_elem_name`
- I think I'll also want to do the same thing for the *count* of the current element (or group), since we'll have to deal with multi-digit numbers. So I'll also initialize `curr_count_digits` to an empty string.
- Then I'll start parsing `formula`:
  - if the current character is an uppercase letter, we're starting to parse a new element name, so we need to "finalize" either the element or group of elements we've been parsing up to this point. I think this is the trickiest case, in terms of actions we take based on characters we encounter, because what we do depends on the previous characters we've encountered.
    - If we just finished parsing an element name, we can finalize it by:
      - incrementing its count in `elem_counts` by the proper value
        - the "proper value" is 1 if `curr_count_digits == ''`, else `int(curr_count_digits)`
      - overwriting `curr_elem_name` with the current character
      - resetting `curr_count_digits` to `''`.
      - **Note**: how to handle the case where `curr_elem_name` is empty, i.e. we're at the beginning of the string -- there are a few options for this, and one might be better based on how I end up structuring other parts of my solution, but a few ideas:
        - initialize `curr_elem_name` to the first letter in `formula`, and then iterate over `formula[1:]`
          - probably not a great idea cause it's possible `formula` could start with parentheses
        - simply accept that we may add an empty string with a count of 1 to `elem_counts`, and `.pop()` it off before we build up the final string to return
          - this seems like the best option, so I'll plan on going with it for now
    - else (we just finished parsing a group of elements):
      - this is trickier, and I think I'll handle groups of elements as part of the process of handling parentheses, which I'll figure out below
  - elif the current character is a lowercase letter, it's part of the element name we're currently building up, so simply add it to `curr_elem_name` and continue on
  - elif the current character is a digit, we're currently building up a count for the preceding elemen (or group of elements), so add it to `curr_count_digits` and continue on
    - since we'll need to do this for both single elements and element groups, I might want to abstract this to a helper function.
  - elif the current character is `(`, we're about to start parsing an element group. The logic for this could be complex so I'll give it its own section. But we'll also need to "finalize" the element/group we've been building up up to this point
  - else (the current character is `)`), we're finishing parsing an element group. Gonna figure out parsing element groups below.

### Handling element groups

- Okay, at first glance I can think of two ways of dealing with this. One is a one-pass solution and the other is a two-pass solution:
  - The one-pass solution involves calling a recursive function each time we encounter a `(`, and returning from it when we encounter its matched `)` (or possibly after we parse the digits following the `)`, if applicable)
  - The two-pass solution involves using the first pass to resolve parentheses by removing them from the `formula` and multiplying any counts inside them as necessary. The second pass would then just require iterating through the `formula` and parsing element names and counts.
- The catch is whether the test cases are going to be actual **real**&mdash;or at least **realistic**&mdash;chemical formulas. If so, then the one-pass solution would be faster. But if they aren't necessarily realistic formulas, we could get something like `((((((((((((((H))))))))))))))` (but with thousands of parentheses), which could cause the one-pass version to hit the recursion limit -- or also just be really slow on contrived test cases.
  - one of the constraints says that "*`formula` is always valid*", but it's not clear whether that means "*syntactically* valid" or "*chemically* valid", i.e., realistic.
- Could I implement the one-pass solution using a stack instead of recursion? Something like:
  - if we encounter a `(`, initialize an empty stack and start pushing characters to it.
  - Keep track of the current "depth" of parentheses by initializing a counter, incrementing it when we push a `(`, and decrementing it when we push a `)`.
  - ... I don't think this would work. Any number of nested parentheses can have multipliers after them, which means we could need to multiply doubly+ nested parentheses multiple times, so this isn't a strict LIFO situation.
- I'm gonna take note of the constraint that says the max length of the formula is 1000 characters, which means the worst possible case is 499 levels of nested parentheses. That's a lot, but Python's default max recursion depth is 1,000, so unless leetcode has its own lower limit, we *should* be okay with a recursive solution.
- Though I'd still like to try to implement the two-pass version

### Hang on a second...

- all of the difficulty with this problem comes from the fact that we have to handle parentheses/element groups in a special/different way because they can be nested and each level of nesting can have its own multiplier, but we won't know what that is until we get to the end of a parenthesized group, so we might have to go back and multiply the counts for elements within nested groups multiple times.
- But what if we knew the multiplier before we parsed each group?
- What if we just parsed the whole `formula` right to left?
- We could just take the inverse of the rules above, in terms of what characters imply what, and I think we could do the whole thing in a single pass. Basically I think we could:
  - initialize:
    -  a `collections.Counter` to track element counts (`elem_counts`)
    -  an empty string to build up the name of the current element (`curr_elem_name`)
    -  an empty string to build up a count for the element/group *to be encountered next*, as we encounter digits (`curr_count_digits`)
    - an integer variable initialized to `1` to tell us what to multiply the count of elements inside the current group by when we increment `elem_counts` (`total_group_multiplier`)
      - **note**: this value is separate from the multiplier given by digits that immediately follow element names -- it only accounts for group-level multipliers
    - a stack to keep track of the individual multipliers for each level of nested parentheses (including 1's for parentheses *without* an explicit a multiplier), so we can `.append()` them and multiply `total_group_multiplier` by them when we encounter `)`s, and `.pop()` them off and divide `total_group_multiplier` by them when we encounter `(`s (`parens_multipliers`)
  - iterate through `reversed(formula)`
      - if the current character is a digit, we're building up a count for the next element or group, so:
        - append/prepend it to `curr_count_digits` and continue
        - **note**: there's a micro-optimization question of whether it's better to build up the counts and element names:
          - as strings, where we add new characters to the beginning of the string, i.e., `curr_count_digits = new_digit + curr_count_digits`
          - as strings, where we add new characters to the end of the string, then `reversed()` the string once we're done building it up
          - as a list, where we insert new characters at the beginning of the list, then `''.join()` the list once we're done building it up
          - as a list, where we append new characters to the end of the list, then `''.join(reversed())` the list once we're done building it up
          - as a `collections.deque`, where we `.appendleft()` new characters and then `''.join()` the deque once we're done building it up
        - I'm not sure which would actually be best here, because on one hand, inserting at the beginning of a list is $O(n)$ where $n$ is the length of the list, buton the other hand $n$ will always be <=2 **if** these are actually real formulas/element names. But I can't tell if they will be.
        - `.reversed()` is also $O(n)$, but it's very fast since it just returns an iterator, and again, $n$ will always be insignificantly small **if** these are real-life examples.
        - `.appendleft()` on a `deque` is $O(1)$, but compared to using strings/lists, it might not actually save time if we're working with a large number of short element names/few-digit numbers, cause the object itself will take longer to initialize than a built-in like `str` or `list`.
        - I'll just pick one of these for now and decide whether or not to micro-optimize later, depending on how my initial solution performs.
    - elif the current character is `)`, we're about to enter a new (potentially nested) group and need to update what we want to multiply element counts within this group by, so:
      - if `curr_count_digits` is non-empty, convert it to an int, set `this_group_multiplier` to it, and reset `curr_count_digits` to an empty string; otherwise, set `this_group_multiplier` to 1
      - multiply `total_group_multiplier` by `this_group_multiplier`
      - push `this_group_multiplier` onto the `parens_multipliers` stack
    - elif the current character is `(`, we're about to exit a group and need to update what we want to multiply element counts within the next layout outward by, so:
      - pop the last element off `parens_multipliers` and divide `total_group_multiplier` by it
    - elif the current character is a lowercase letter, we're building up the name of an element, so add it to `curr_elem_name` and continue
      - **if** the test cases contain only real element names, we could simply *set* `curr_elem_name` to the current character, rather than appending/prepending it, since we know it can only ever be the 2nd and last character in an element name
      - **note**: although `curr_count_digits` might be non-empty at this point (if the element was 2+ letters and followed by a number), we don't need to deal with it in this branch since all elements will start with an upercase letter, so it'll be easier to always just deal with it there
    - else (the current character is an uppercase letter), we've finished building up an element name, so:
      - if `curr_count_digits` is non-empty, convert it to an int, set `this_elem_multiplier` to it, and reset `curr_count_digits` to an empty string; otherwise, set `this_elem_multiplier` to 1.
      - append/prepend the character to `curr_elem_name`
      - increment the count of `curr_elem_name` in `elem_counts` by `this_elem_multiplier * total_group_multiplier`
        - **note**: remember to reverse the name of the element if building it up by appending rather than prepending
      - reset `curr_elem_name` to an empty string
  - we now have the full set of element counts in `elem_counts`, so we need to iterate over a `sorted()` version of it, and build up the string we want to return
- I'm gonna try implementing this version

## Refining the problem, round 2 thoughts

## Attempted solution(s)

### Submission 1

```python
class Solution:
    def countOfAtoms(self, formula: str) -> str:
        elem_counts = Counter()
        curr_elem_name = ''
        curr_count_digits = ''
        total_group_multiplier = 1
        parens_multipliers = []

        for char in reversed(formula):
            if char.isdigit():
                curr_count_digits = char + curr_count_digits
            elif char == ')':
                if curr_count_digits:
                    this_group_multiplier = int(curr_count_digits)
                    curr_count_digits = ''
                else:
                    this_group_multiplier = 1
                total_group_multiplier *= this_group_multiplier
                parens_multipliers.append(this_group_multiplier)
            elif char == '(':
                total_group_multiplier //= parens_multipliers.pop()
            elif char.islower():
                curr_elem_name = char + curr_elem_name
            else:
                if curr_count_digits:
                    this_elem_multiplier = int(curr_count_digits)
                    curr_count_digits = ''
                else:
                    this_elem_multiplier = 1
                curr_elem_name = char + curr_elem_name
                elem_counts[curr_elem_name] += this_elem_multiplier * total_group_multiplier
                curr_elem_name = ''

        return ''.join([elem + str(count) if count > 1 else elem for elem, count in sorted(elem_counts.items())])
```

![](https://github.com/user-attachments/assets/a3818b08-d08c-4d67-a3a0-75dedd7916cf)

I'm a bit surprised it's that comparatively slow... maybe prepending to the strings is taking more time than I thought. I'm gonna switch to using `collections.deque` and see if that improves it.

### Submission 2

```python
class Solution:
    def countOfAtoms(self, formula: str) -> str:
        elem_counts = Counter()
        curr_elem_name = deque()
        curr_count_digits = deque()
        total_group_multiplier = 1
        parens_multipliers = []

        for char in reversed(formula):
            if char.isdigit():
                curr_count_digits.appendleft(char)
            elif char == ')':
                if curr_count_digits:
                    this_group_multiplier = int(''.join(curr_count_digits))
                    curr_count_digits = deque()
                else:
                    this_group_multiplier = 1
                total_group_multiplier *= this_group_multiplier
                parens_multipliers.append(this_group_multiplier)
            elif char == '(':
                total_group_multiplier //= parens_multipliers.pop()
            elif char.islower():
                curr_elem_name.appendleft(char)
            else:
                if curr_count_digits:
                    this_elem_multiplier = int(''.join(curr_count_digits))
                    curr_count_digits = deque()
                else:
                    this_elem_multiplier = 1
                curr_elem_name.appendleft(char)
                elem_counts[''.join(curr_elem_name)] += this_elem_multiplier * total_group_multiplier
                curr_elem_name = deque()

        return ''.join([elem + str(count) if count > 1 else elem for elem, count in sorted(elem_counts.items())])
```

![](https://github.com/user-attachments/assets/eca1261b-47fc-4039-9258-0adfec20e414)

Nice 😎 🏃‍♂️💨
