# [Problem 273: Integer to English Words](https://leetcode.com/problems/integer-to-english-words/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- I think this problem will need to be solved partly by hard-coding some number-to-word mappings, and partly by applying patterns
- We'll need to start parsing by converting the number (integer) to a string
- There's also a recursive component-- e.g., 12345 needs to be split into:
    - 12 (parsed as "Twelve", recursively using the "hundreds" parsing code) + " Thousand"
    - 345 (parsed as "Three Hundred Forty Five")
- First, let's write a function for parsing 0--9 (single digits)
- Then we can write a function for parsing 10--99 (double digits)
    - 10--19 need to be coded as special cases
    - After that, we just need to hard code in Twenty, Thirty, ..., Ninety + a call to the function for parsing single digits
- To parse hundreds, we simply:
    - Parse the single (leading) number ("" if 0) and add " Hundred"
    - Then add " " + parse of the remaining two digits
- To parse thousands, we can parse hundreds and add " Thousand", and similarly for parsing millions and billions
    - We don't need to go beyond billions, since `0 <= num <= 2^31 - 1`
    - To do this efficiently, let's write a base function that includes an argument for the prefix
- Then we can just call the functions in blocks of 3 digits:
    - First the last 3: parse using "hundreds"
    - Next, the second-to-last 3: parse using "thousands" and prepend to the result
    - Next, the third-to-last 3: parse using "millions" and prepend to the result
    - Finally, the fourth-to-last "3": parse using "billions" and prepend to the result
- The main "trickiness" in this problem will come from making sure we cover all of the edge cases.  We'll need to test carefully.

## Refining the problem, round 2 thoughts
- We'll need the following functions (note: here I'm being sloppy with notation by not being explicit about converting to ints or strs, but in the actual implementation we'll need to handle type casting correctly):
    - `ParseSingle(x)`: maps single digits 0--9 onto words (hard code)
    - `ParseDouble(x)`: maps double digits 10--99 onto words:
        - Hard code 10--19
        - Hard code multiples of 10 between 20 and 90, inclusive
        - If `x > 19` and `x % 10 != 0` then return `ParseDouble(10 * x // 10) + " " + ParseSingle(x[1])`
    - `ParseTriple(x)`: maps triple digits onto words:
        - This is straightforward:
            - If `len(x) == 1` return `ParseSingle(x)`
            - Else if `len(x) == 2` return `ParseDouble(x)`
            - Else if `x % 100 == 0` return `ParseSingle(x[0]) + " Hundred"`
            - Otherwise return `ParseSingle(x[0] + " " + suffix + " Hundred " + ParseDouble([x[1:]])
    - `ParseThousands(x)`:
        - return `ParseTriple(x) + " Thousand"`
    - `ParseMillions(x)`:
        - return `ParseTriple(x) + " Million"`
    - `ParseBillions(x)`:
        - return `ParseTriple(x) + " Billion"`
    - `Parse(x)`:
        - Break `x` into chunks of 3 (starting from the end)-- we could just hard code in the cases, since there aren't many of them
        - If `1 <= len(x) <= 3`:
            - return `ParseTriple(x)`
        - Elif `4 <= len(x) <= 6`:
            - return `ParseThousands(x[-6:-3]) + " " + ParseTriple(x[-3:])`
        - Elif `7 <= len(x) <= 9`:
            - return `ParseMillions(x[-9:-6]) + " " + ParseThousands(x[-6:-3]) + " " + ParseTriple(x[-3:])`
        - Elif `10 <= len(x) <= 12`:
            - return `ParseBillions(x[-12:-9]) + " " + ParseMillions(x[-9:-6]) + " " + ParseThousands(x[-6:-3]) + " " + ParseTriple(x[-3:])`
        - Note: actually, I think we can do this more cleanly by separately parsing the billions, millions, thousands, and hundreds, and then joining everything together.  This will also make it easier to handle spacing.
- Let's go with this.  Again, though, we're going to need to test everything carefully using a bunch of example cases to be sure we've accounted for everything needed.
## Attempted solution(s)
```python
class Solution:
    def numberToWords(self, num: int) -> str:
        if num == 0:
            return "Zero"
        
        def ParseSingle(x):
            map = {'0': 'Zero', '1': 'One', '2': 'Two', '3': 'Three', '4': 'Four', '5': 'Five',
                   '6': 'Six', '7': 'Seven', '8': 'Eight', '9': 'Nine'}
            return map[x]
        
        def ParseDouble(x):
            map = {'10': 'Ten', '11': 'Eleven', '12': 'Twelve', '13': 'Thirteen', '14': 'Fourteen', '15': 'Fifteen',
                   '16': 'Sixteen', '17': 'Seventeen', '18': 'Eighteen', '19': 'Nineteen',
                   '20': 'Twenty', '30': 'Thirty', '40': 'Forty', '50': 'Fifty',
                   '60': 'Sixty', '70': 'Seventy', '80': 'Eighty', '90': 'Ninety'}
            if x in map:
                return map[x]
            else:
                return map[str(10 * (int(x) // 10))] + " " + ParseSingle(x[1])
        
        def ParseTriple(x):
            if len(x) == 1:
                return ParseSingle(x)
            elif len(x) == 2:
                return ParseDouble(x)
            elif int(x[0]) == 0:
                return ParseDouble(x[1:])
            elif int(x[1:]) == 0:
                return ParseSingle(x[0]) + " Hundred"
            else:
                return ParseSingle(x[0]) + " Hundred " + ParseDouble(x[1:])
        
        def ParseThousands(x):
            if int(x) == 0:
                return ""
            return ParseTriple(x) + " Thousand"
        
        def ParseMillions(x):
            if int(x) == 0:
                return ""
            return ParseTriple(x) + " Million"
        
        def ParseBillions(x):
            if int(x) == 0:
                return ""
            return ParseTriple(x) + " Billion"
        
        x = str(num)
        n = len(x)
        
        # Breaking into groups of 3 digits
        billion = x[-12:-9] if n > 9 else ""
        million = x[-9:-6] if n > 6 else ""
        thousand = x[-6:-3] if n > 3 else ""
        hundred = x[-3:]
        
        result = []
        if billion:
            result.append(ParseBillions(billion))
        if million:
            result.append(ParseMillions(million))
        if thousand:
            result.append(ParseThousands(thousand))
        if hundred:
            result.append(ParseTriple(hundred))
        
        return ' '.join([x for x in result if len(x) > 0])
```
- Given test cases pass
- Let's try a bunch of other cases:
    - 0: pass
    - 10: pass
    - 2918473: pass
    - 1478349587: pass
    - 49: pass
- Ok...let's submit this!

![Screenshot 2024-08-06 at 11 00 48 PM](https://github.com/user-attachments/assets/51886cce-4ee9-4c49-b108-5e08bcc0478d)

Uh oh...looks like I've missed something 😞.  Womp womp 🎺.  Let's see what's going on...
- I think the issue is with `ParseDouble`: I forgot to handle cases where (if we're calling `ParseDouble` from `ParseTriple`) the result of `int(x) // 10` could be 0.  I'm just going to hard code in that case by mapping `"0"` to `""` inside of `ParseDouble`.
- However, when I do that, the spacing gets messed up.  Rather than fixing it in a clean way (🙃) I'll just "hack" the solution at the end by splitting/joining the final result.
- Revised solution:

```python
class Solution:
    def numberToWords(self, num: int) -> str:
        def ParseSingle(x):
            map = {'0': 'Zero', '1': 'One', '2': 'Two', '3': 'Three', '4': 'Four', '5': 'Five',
                   '6': 'Six', '7': 'Seven', '8': 'Eight', '9': 'Nine'}
            return map[x]
        
        def ParseDouble(x):
            map = {'10': 'Ten', '11': 'Eleven', '12': 'Twelve', '13': 'Thirteen', '14': 'Fourteen', '15': 'Fifteen',
                   '16': 'Sixteen', '17': 'Seventeen', '18': 'Eighteen', '19': 'Nineteen',
                   '20': 'Twenty', '30': 'Thirty', '40': 'Forty', '50': 'Fifty',
                   '60': 'Sixty', '70': 'Seventy', '80': 'Eighty', '90': 'Ninety', "0": ""}
            if x in map:
                return map[x]
            else:
                return map[str(10 * (int(x) // 10))] + " " + ParseSingle(x[1])
        
        def ParseTriple(x):
            if len(x) == 1:
                return ParseSingle(x)
            elif len(x) == 2:
                return ParseDouble(x)
            elif int(x[0]) == 0:
                return ParseDouble(x[1:])
            elif int(x[1:]) == 0:
                return ParseSingle(x[0]) + " Hundred"
            else:
                return ParseSingle(x[0]) + " Hundred " + ParseDouble(x[1:])
        
        def ParseThousands(x):
            if int(x) == 0:
                return ""
            return ParseTriple(x) + " Thousand"
        
        def ParseMillions(x):
            if int(x) == 0:
                return ""
            return ParseTriple(x) + " Million"
        
        def ParseBillions(x):
            if int(x) == 0:
                return ""
            return ParseTriple(x) + " Billion"
        
        x = str(num)
        n = len(x)
        
        # Breaking into groups of 3 digits
        billion = x[-12:-9] if n > 9 else ""
        million = x[-9:-6] if n > 6 else ""
        thousand = x[-6:-3] if n > 3 else ""
        hundred = x[-3:]
        
        result = []
        if billion:
            result.append(ParseBillions(billion))
        if million:
            result.append(ParseMillions(million))
        if thousand:
            result.append(ParseThousands(thousand))
        if hundred:
            result.append(ParseTriple(hundred))
        
        result = ' '.join([x for x in result if len(x) > 0])
        return ' '.join(result.split())  # clean up white spaces
```
- Submitting without checking anything!! This is life in the fast lane... ⚠️ 🚗 ⚠️

![Screenshot 2024-08-06 at 11 14 45 PM](https://github.com/user-attachments/assets/f446ebc6-3c5c-4dbc-aad0-dfaa41615556)

Uh oh.  What have I done here... "One Thousand Zero" definitely isn't a thing...🤦  Gah!!

Ok, let's try to be careful here...

## More notes...
- I think the problem is because, in `ParseSingle`, "0" should actually *not* map to "Zero" if that function is called from the `ParseDouble` function.  I think I can just add a flag to handle this.

```python
class Solution:
    def numberToWords(self, num: int) -> str:
        def ParseSingle(x, ignore_zero=False):
            map = {'0': 'Zero', '1': 'One', '2': 'Two', '3': 'Three', '4': 'Four', '5': 'Five',
                   '6': 'Six', '7': 'Seven', '8': 'Eight', '9': 'Nine'}
            if x == "0" and ignore_zero:
                return ""
            return map[x]                
        
        def ParseDouble(x):
            map = {'10': 'Ten', '11': 'Eleven', '12': 'Twelve', '13': 'Thirteen', '14': 'Fourteen', '15': 'Fifteen',
                   '16': 'Sixteen', '17': 'Seventeen', '18': 'Eighteen', '19': 'Nineteen',
                   '20': 'Twenty', '30': 'Thirty', '40': 'Forty', '50': 'Fifty',
                   '60': 'Sixty', '70': 'Seventy', '80': 'Eighty', '90': 'Ninety', "0": ""}
            if x in map:
                return map[x]
            else:
                return map[str(10 * (int(x) // 10))] + " " + ParseSingle(x[1], ignore_zero=True)
        
        def ParseTriple(x):
            if len(x) == 1:
                return ParseSingle(x)
            elif len(x) == 2:
                return ParseDouble(x)
            elif int(x[0]) == 0:
                return ParseDouble(x[1:])
            elif int(x[1:]) == 0:
                return ParseSingle(x[0]) + " Hundred"
            else:
                return ParseSingle(x[0]) + " Hundred " + ParseDouble(x[1:])
        
        def ParseThousands(x):
            if int(x) == 0:
                return ""
            return ParseTriple(x) + " Thousand"
        
        def ParseMillions(x):
            if int(x) == 0:
                return ""
            return ParseTriple(x) + " Million"
        
        def ParseBillions(x):
            if int(x) == 0:
                return ""
            return ParseTriple(x) + " Billion"
        
        x = str(num)
        n = len(x)
        
        # Breaking into groups of 3 digits
        billion = x[-12:-9] if n > 9 else ""
        million = x[-9:-6] if n > 6 else ""
        thousand = x[-6:-3] if n > 3 else ""
        hundred = x[-3:]
        
        result = []
        if billion:
            result.append(ParseBillions(billion))
        if million:
            result.append(ParseMillions(million))
        if thousand:
            result.append(ParseThousands(thousand))
        if hundred:
            result.append(ParseTriple(hundred))
        
        result = ' '.join([x for x in result if len(x) > 0])
        return ' '.join(result.split())  # clean up white spaces
```
- Ok...submitting again 🤞...

![Screenshot 2024-08-06 at 11 29 07 PM](https://github.com/user-attachments/assets/9ef5cfb7-c75a-444a-87b5-b977ef5fa42e)

Finally solved 🥳!
