# [Problem 592: Fraction Addition and Subtraction](https://leetcode.com/problems/fraction-addition-and-subtraction/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- First we'll need to convert all of the fractions to a common denominator.  The simplest way to do this is:
    - Take all of the unique denominators and multiply them together to get the new denominators
        - We can save some time-- first sort the denominators in ascending order.  Then, as we're adding new denominators, check whether the new denominator `d` is evenly divisible by any of the denominators that have been added so far.  If so, divide `d` by those factors in the list before adding it (assuming it's not already in the list).
    - Take each numerator (`n`) and divide it by (`common_denominator / d`), where `d` is the original denominator
- Next, we'll add/subtract the adusted numerators to get the result's numerator
- Then at the end, we'll need to reduce the fraction by dividing both the numerator and denominator of the result by any denominators in the `unique_denominators` list that they are both cleanly divisible by (e.g., `n % x == 0 and d % x == 0`)
- With this approach we don't really need to worry about the special case where the answer is an integer, since the "reducing the fractions" step will result in 1 in that case, which is the desired format

## Refining the problem, round 2 thoughts
- Things to solve:
    - How do we get all of the numerators, denominators, and coefficients?  We could just loop through and parse it all manually by searching for `"/"` characters.  Something like this:
    ```python
    def parse(expression):
        numerators = []
        denominators = []

        digits = '0123456789'
        operators = '+-'
        
        if expression[0] in digits:
            expression = '+' + expression
        
        sign = expression[0]
        expression = expression[1:]
        i = 0
        current_number = ''
        while i < len(expression):
            if expression[i] in digits:
                current_number += expression[i]
            else:
                if len(numerators) == len(denominators):
                    current_number = sign + current_number
                    numerators.append(int(current_number))
                else:
                    denominators.append(int(current_number))
                current_number = ''

            if expression[i] in operators:
                sign = expression[i]
            
            i += 1
        denominators.append(int(current_number))
        
        return numerators, denominators
    ```
    - How do we get the common denominator?
    ```python
    import math
    
    def common_denominator(denoms):
        unique_denoms = []
        for d in sorted(denoms):
            for x in unique_denoms:
                if d % x == 0:
                    d /= x
            if d not in unique_denoms:
                unique_denoms.append(d)
        return int(math.prod(unique_denoms)), unique_denoms
    ```
    - Convert numerators to use the common denominator and sum them together
    ```python
    def convert_and_sum(numerators, denominators, common_denom, unique_denoms):
        x = 0
        for n, d in zip(numerators, denominators):
            x += int(n * (common_denom / d))

        # now see if we can divide the sum and common denominator by a common number
        for d in unique_denoms:
            if (x % d == 0) and (common_denom % d == 0):
                x /= d
                common_denom /= d

        return f'{int(x)}/{int(common_denom)}'
    ```
    - I think that's everything; let's put the pieces together!

## Attempted solution(s)
```python
import math

class Solution:
    def fractionAddition(self, expression: str) -> str:
        def parse(expression):
            numerators = []
            denominators = []
    
            digits = '0123456789'
            operators = '+-'
            
            if expression[0] in digits:
                expression = '+' + expression
            
            sign = expression[0]
            expression = expression[1:]
            i = 0
            current_number = ''
            while i < len(expression):
                if expression[i] in digits:
                    current_number += expression[i]
                else:
                    if len(numerators) == len(denominators):
                        current_number = sign + current_number
                        numerators.append(int(current_number))
                    else:
                        denominators.append(int(current_number))
                    current_number = ''
    
                if expression[i] in operators:
                    sign = expression[i]
                
                i += 1
            denominators.append(int(current_number))
            
            return numerators, denominators

        def common_denominator(denoms):
            unique_denoms = []
            for d in sorted(denoms):
                for x in unique_denoms:
                    if d % x == 0:
                        d /= x
                if d not in unique_denoms:
                    unique_denoms.append(d)
            return int(math.prod(unique_denoms)), unique_denoms

        def convert_and_sum(numerators, denominators, common_denom, unique_denoms):
            x = 0
            for n, d in zip(numerators, denominators):
                x += int(n * (common_denom / d))
    
            # now see if we can divide the sum and common denominator by a common number
            for d in unique_denoms:
                if (x % d == 0) and (common_denom % d == 0):
                    x /= d
                    common_denom /= d
    
            return f'{int(x)}/{int(common_denom)}'

        nums, denoms = parse(expression)
        common_denom, unique_denoms = common_denominator(denoms)
        return convert_and_sum(nums, denoms, common_denom, unique_denoms)
```
- Given test cases pass
- Let's make up some other examples:
```python
n_terms = 10
def random_op():
   if random.random() > 0.5:
      return '+'
   else:
      return '-'
expression = ''.join([f'{random_op()}{random.randint(0, 10)}/{random.randint(1, 10)}' for _ in range(n_terms)])
if expression[0] == '+':
   expression = expression[1:]
print(expression)
```

- `expression = "-8/6-3/1+2/1+5/10-10/10+7/4+0/9-4/10+7/5+6/1"`: pass
- `expression = "-2/9+6/2+9/1-9/10-4/10-9/6-0/5+7/5+4/4-6/4"`: fail!  returns "99/10" instead of "889/90" -- maybe a rounding error?
    - I'm noticing a potential optimization: if the numerator is 0, it's actually not critical that we add the denominator.  We can just add "1" to the denominator list instead.
    - The `common_denominator` function doesn't seem to be working correctly.  For this example, it gives the common denominator as "30" but clearly this isn't correct, since neither 9 nor 4 divide evenly into 30.  The correct answer is "270".  So what's going wrong... 🤔.  Let's debug:
    ```python
    import math
        
    def common_denominator(denoms):    
        unique_denoms = []
        for d in denoms:
            if d not in unique_denoms:
                unique_denoms.append(d)
    
        print(f'sorted unique denominators: {list(sorted(unique_denoms))}')
        reduced_denoms = []
        for d in sorted(unique_denoms):
            print(f'considering next: {d}')
            if d == 1:
                print('\tskipping (denominator is 1)')
                continue
            for x in reduced_denoms:
                if d % x == 0:
                    print(f'\tdivisible by {x}')
                    d /= x
                    d = int(d)
                    print(f'\tnew denominator: {d}')
            if d not in reduced_denoms:
                reduced_denoms.append(d)
                print(f'\tadding {d} to reduced_denoms; updated list: {reduced_denoms}')
            else:
                print(f'\t{d} has already been added to the list; skipping')
        return int(math.prod(reduced_denoms))
    ```
    - For the given example, I'm getting this output:
    ```
    sorted unique denominators: [1, 2, 4, 5, 6, 9, 10]
    considering next: 1
        skipping (denominator is 1)
    considering next: 2
        adding 2 to reduced_denoms; updated list: [2]
    considering next: 4
        divisible by 2
        new denominator: 2
        2 has already been added to the list; skipping
    considering next: 5
        adding 5 to reduced_denoms; updated list: [2, 5]
    considering next: 6
        divisible by 2
        new denominator: 3
        adding 3 to reduced_denoms; updated list: [2, 5, 3]
    considering next: 9
        divisible by 3
        new denominator: 3
        3 has already been added to the list; skipping
    considering next: 10
        divisible by 2
        new denominator: 5
        divisible by 5
        new denominator: 1
        adding 1 to reduced_denoms; updated list: [2, 5, 3, 1]
    ```
    - So now I can see what the issue is: the `d % x` test is actually filtering out the wrong numbers.  E.g., when we consider 4, the 4 should replace the 2 instead of skipping the 4 because it's divisible by 2.  Similarly, when we get to 9, the 9 should replace the 3 instead of skipping 9 because it's dividible by 3.  So let's rewrite this accordingly (with debug statements):
    ```python
    import math
        
    def common_denominator(denoms):    
        unique_denoms = []
        for d in denoms:
            if d not in unique_denoms:
                unique_denoms.append(d)
    
        print(f'sorted unique denominators: {list(sorted(unique_denoms))}')
        reduced_denoms = []
        for d in sorted(unique_denoms):
            print(f'considering next: {d}')
            if d == 1:
                print('\tskipping (denominator is 1)')
                continue
            for i, x in enumerate(reduced_denoms):
                if d % x == 0:
                    print(f'\tdivisible by {x}; replacing {x} with {d}')
                    if d not in reduced_denoms:
                      reduced_denoms[i] = d
                      print(f'\tupdated list: {reduced_denoms}')                  
            if d not in reduced_denoms:
              reduced_denoms.append(d)
              print(f'\tupdated list: {reduced_denoms}')
        reduced_denoms = list(set(reduced_denoms))
        print('after removing duplicates: ', reduced_denoms)
        return int(math.prod(reduced_denoms))
    ```
    - For the "working example," we get:
    ```
    sorted unique denominators: [1, 2, 4, 5, 6, 9, 10]
    considering next: 1
        skipping (denominator is 1)
    considering next: 2
        updated list: [2]
    considering next: 4
        divisible by 2; replacing 2 with 4
        updated list: [4]
    considering next: 5
        updated list: [4, 5]
    considering next: 6
        updated list: [4, 5, 6]
    considering next: 9
        updated list: [4, 5, 6, 9]
    considering next: 10
        divisible by 5; replacing 5 with 10
        updated list: [4, 10, 6, 9]
    after removing duplicates:  [9, 10, 4, 6]
    ```
    - So...actually, this isn't correct either.  The 10, 4, and 6 should all be divided by 2.  From some googling, I see that there's actually a built-in function that will be useful here: `math.gcd` finds the greatest common divisor of two integers.  So assuming we don't have any overflow issues, there's a much simpler solution:
        - Multiply all of the unique denominators together to get the common denominator
        - In the final step, use `math.gcd` to divide both the numerator and denominator by their greatest common divisor so that the fraction is reduced properly.
- Revised solution:
```python
import math

class Solution:
    def fractionAddition(self, expression: str) -> str:
        def parse(expression):
            numerators = []
            denominators = []
    
            digits = '0123456789'
            operators = '+-'
            
            if expression[0] in digits:
                expression = '+' + expression
            
            sign = expression[0]
            expression = expression[1:]
            i = 0
            current_number = ''
            while i < len(expression):
                if expression[i] in digits:
                    current_number += expression[i]
                else:
                    if len(numerators) == len(denominators):
                        current_number = sign + current_number
                        numerators.append(int(current_number))
                    else:
                        denominators.append(int(current_number))
                    current_number = ''
    
                if expression[i] in operators:
                    sign = expression[i]
                
                i += 1
            denominators.append(int(current_number))
            
            return numerators, denominators

        def common_denominator(denoms):
            return math.prod(list(set(denoms)))

        def convert_and_sum(numerators, denominators, common_denom):
            x = 0
            for n, d in zip(numerators, denominators):
                x += int(n * (common_denom / d))
    
            # reduce the fraction
            y = math.gcd(x, common_denom)
            x /= y
            common_denom /= y            
    
            return f'{int(x)}/{int(common_denom)}'
        
        nums, denoms = parse(expression)
        common_denom = common_denominator(denoms)
        return convert_and_sum(nums, denoms, common_denom)
```
- Now all of these test cases work!
- Let's try some more...
    - `expression = "-0/7+2/7+5/4-3/8+6/9-4/5-4/10+2/7+0/3-2/9"`: pass
    - `expression = "8/9+8/9+10/9-4/8+8/1-2/4+1/6-2/2-0/4+7/5"`: pass
- Ok, submitting!

![Screenshot 2024-08-23 at 12 07 43 AM](https://github.com/user-attachments/assets/28057729-c3bf-4ef5-9043-8c087711b561)

Solved 🥳!
