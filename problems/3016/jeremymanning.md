# [Problem 3016: Minimum Number of Pushes to Type Word II](https://leetcode.com/problems/minimum-number-of-pushes-to-type-word-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- We have 8 unique "keys" to work with (i.e., the numbers 2 -- 9)
- I think we should start by counting up the number of occurances of each character.  We can store the counts in a hash table.  This takes $O(n)$ time, where $n$ is the length of the word.
- Then we can sort characters in descending order of occurance.  This takes $O(c \log c)$ time, where $c$ is the number of unique characters.  At most $c$ could be 26, so this is (roughly) constant time.
- The first 8 most common characters get "primary" mappings
- The second 8 most common characters get "secondary" mappings
- The third 8 most common characters get "tertiary" mappings
- The remaining (up to 2) most common characters get "quaternary" mappings
- We can store the mappings (we just need the costs, not the actual key mappings) in a hash table
- Then we can count up (and then return) the final score using a running sum where we tally up each character's cost by looking it up in the cost hash table.  This (again) takes $O(n)$ time, so the full algorithm is still $O(n)$.
    - Actually-- we could just loop through the hash table of counts to do this more quickly (e.g., `total_cost += counts[c] * cost[c]`)
- The only somewhat tricky part is hashing out the mappings to get the costs.  Let's think through how that could work...

## Refining the problem, round 2 thoughts
- Given the sorted (in descending order) unique characters, we can assign "costs" per character as follows:
```python
n_keys = 8
costs = {}
for i, c in enumerate(sorted_chars):
    costs[c] == (i // n_keys) + 1
```
- I think we have enough to implement the full solution...

## Attempted solution(s)
```python
class Solution:
    def minimumPushes(self, word: str) -> int:
        # first count the number of times each character appears
        counts = {}
        for c in word:
            if c in counts:
                counts[c] += 1
            else:
                counts[c] = 1

        # now sort characters in descending order of the number of instances
        chars = [x[0] for x in sorted(counts.items(), key=lambda x: x[1], reverse=True)]

        # assign per-character costs
        n_keys = 8
        costs = {}
        for i, c in enumerate(chars):
            costs[c] = (i // n_keys) + 1

        # now compute the final cost
        total_cost = 0
        for c, n in counts.items():
            total_cost += counts[c] * costs[c]

        return total_cost
```
- Given test cases pass
- Let's make up some new test cases by choosing random characters:
    - `word = "glnzwujbyhhnjbhilhtqjmhnktjtoarvcarpuqflubisaevaydpgngdagmumalrlxwbtnumoqiuisvkkdvclvuujlhdyblcgpjgh"`: pass
    - `word = "bqtzntmeeoybtaucsoyjfoeoyqufggsqyqkifdxmgaadxobokbkcdvtdjdaoxusdkbalkbayhtimzhtvalbgiyeyvayforynicgzfkwcualncyeqqwoeatqrnwvsjfjzcfclqrujwbinigppeyhwgmzvhcsjwkhwaqyvkfjqdeyakuhzjqgkbotsaqhvaskyyeocghtlnlfrcisagtlegupjqgjwvmxvmrjbxsnwpgimhpowgjavxvofqfwvtufibnuxhvwcndzcudakdzrrvfeykbytffdbvtkulfagtzarkuxtmnodtfxixnxpqjumpkzwymvkfecajjlazejugqifidyfdajqfjpftbeqeaummnkgpvnqfdlmbaiueiyvrhdupgvwnianvnyilipnujmpfmhcrubdlvqdslsgdukncrqimafvomuhrtpxcwisqhjhwgnierrgjhxhehkqdfjignutuluimlgpgcerxzsuvjyhkrjomnsrbeilotthlahcwjxcziyrkexdhogrebxxmqcigxicypeujqgdelsbyojloomsgifvsqtdegtvswnznkrdchzxnvbojnahefduzsdouuiixsgbchapavipuuumbrpkgsuhfejmlwxvjxpruwsrjbhhpnkspwwvnzhotspudnnlaiqguqfobrrybbrfziqfcetgyyxyadlicaybjpvaqttwkialbfptbfgptlbbotkviyfgsmbjsliktconbkflqfaahzxawzeckbvrbpbfxqhrigqkpeuiehgrponiqibdhfevulnfwqsajdnxgiysikcsujmxvtwpvznrummysbnophmmqnxbqbnqovbahpdbpnqzwmlymsmjmximzvvtmxudgtvfcthzkvrrrlpyotgixtmbrxnryypjguuaxuvylfthigtospjnllmexfaspoiicrxqhyluveosigeidnijlhixmheholsdsvcpxunpoffyueri"`: pass
    - `word = "jjkezznflnsqzlwxmzatthemwtmvogsiwbwfdmmvwyozulmpobukdrihiotnjtehdwqgxdjsunoggeeweqtipmsgnddonlkypowsurvvbimgreiwbeoznsapncruwuqymamydccuryjhceanjdhrpwugfhawuvdyqiwxrhycmzzvlucchabetsrrxmqnnxdiqzulduutatvxcogrgqqywfmjtraithkqqydmbbysjphgbzosufyicmprvrcvgggiznsqdgrplesewdvoqpeircehsbznddrxzxzxhhectjylmbexyazzredznxxcmnydbdkfwgaddvasixsijtulqzhoaxuubqnazfysbyoprmnqhoopndhwkmljsvnxkdufsldymchxqgqrgcutygfxurvtqnkyknfutprmhstayofmfnhdhbfegskxmnwujexzkbprhsadakiavnlrarfmwolsnzgozkmzzhdgihwfdzqnyqmrrjiemqvfckvvqsxnesslyzcakaalqhtqftpclepvyayvgrgqpngxgdznijgikqosuwvnnulhjtpeuxszvezujwvoymrcttmyftjuugcvjmdzlnsdeekvbqkhkvhgfokwtgpwqvymazibayinuseqmmxxfjrkysqeeqgkyoiqenkmgubnehuenrbywuqekvbgtuancusvxgofswpnhoiqqqlyisgnlzjezrswzbzhjfbpczieqsmbkyqjplqsrkpwhkeuxorwkewbctkuxvhuymgkfzvdpskkmukloriplwrowpbnfnogapxvqdyvfottvkjgxhcciqioadlxewinrxfwqprphgdiozpzivfkcpdswylaopcphpxzgrvqriezzuszagivuijwxgwcnqlmgbcyrnflhdefxqtdtysfqwfdmdsneiqswmxiwaiwkgcitgrjlllvxblvbeajrxkyjojdhcupnffobcimywtefmgnaeirrgganmue"`: pass
- Looks OK; submitting...

![Screenshot 2024-08-05 at 10 34 21 PM](https://github.com/user-attachments/assets/94cb71f4-79f8-444f-9522-544b7a8c1810)

I'm surprised it's so slow relative to other solutions...but I'll take it-- solved!

