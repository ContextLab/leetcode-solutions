# [Problem 3433: Count Mentions Per User](https://leetcode.com/problems/count-mentions-per-user/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to simulate users going offline for 60 time units and messages that mention users. Each message can be "ALL" (mention every user regardless of online state), "HERE" (mention only currently online users), or a sequence of "id<number>" tokens (which can include duplicates and mention offline users too). Important detail: status changes (OFFLINE) at a timestamp are processed before any MESSAGE at the same timestamp. That implies we should process events in timestamp order and ensure OFFLINE events at the same timestamp are handled before MESSAGE events. A straightforward approach is to track, for each user, until what time they remain offline (offline_until). When offline_until > t the user is offline at time t; otherwise they are online.

Since constraints are small (<=100 users, <=100 events), a simple simulation with sorting events by (timestamp, type-priority) will be efficient and easy to implement.

## Refining the problem, round 2 thoughts
- We should sort events by timestamp and ensure OFFLINE events come before MESSAGE events at the same timestamp (tie-breaker).
- For OFFLINE events: set offline_until[user] = timestamp + 60.
- For MESSAGE events:
  - If token == "ALL": increment every user's mention count.
  - If token == "HERE": increment every user with offline_until <= timestamp (i.e., online).
  - Else: split the string by spaces and for each "idX" increment that user's count (duplicates counted).
- Edge cases:
  - Input might already be sorted, but we explicitly sort to enforce the tie-breaker rule.
  - OFFLINE events are guaranteed to reference an online user at that moment (so no double-offline).
- Complexity: Sorting O(E log E) where E <= 100 negligible. Processing each event is at worst O(U) per event (for ALL/HERE) or O(k) for explicit ids, so overall O(E * max(U, k)). Space O(U).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def countMentions(self, numberOfUsers: int, events: List[List[str]]) -> List[int]:
        # Parse events to (timestamp:int, type:str, payload:str)
        parsed = []
        for ev in events:
            typ, ts_str, payload = ev
            ts = int(ts_str)
            parsed.append((ts, typ, payload))
        # Sort by timestamp, with OFFLINE before MESSAGE at same timestamp
        # OFFLINE priority = 0, MESSAGE priority = 1
        parsed.sort(key=lambda x: (x[0], 0 if x[1] == "OFFLINE" else 1))
        
        mentions = [0] * numberOfUsers
        # offline_until[i] stores the time when user i becomes online again.
        # user is offline at time t iff offline_until[i] > t
        offline_until = [0] * numberOfUsers  # initially 0 => online for all t >= 0
        
        for ts, typ, payload in parsed:
            if typ == "OFFLINE":
                user_id = int(payload)
                # user goes offline at ts for 60 units -> back online at ts + 60
                offline_until[user_id] = ts + 60
            else:  # MESSAGE
                if payload == "ALL":
                    # mention all users regardless of online status
                    for i in range(numberOfUsers):
                        mentions[i] += 1
                elif payload == "HERE":
                    # mention only online users at this timestamp
                    for i in range(numberOfUsers):
                        if offline_until[i] <= ts:
                            mentions[i] += 1
                else:
                    # list of id<number> tokens, separated by single spaces
                    tokens = payload.split()
                    for tok in tokens:
                        # tok format is "id<number>"
                        if tok.startswith("id"):
                            uid = int(tok[2:])
                            mentions[uid] += 1
                        else:
                            # defensive: shouldn't happen per problem statement
                            pass
        return mentions
```
- Notes:
  - We sort events by (timestamp, OFFLINE-before-MESSAGE) to respect the rule that status changes at a timestamp are applied before messages at the same timestamp.
  - offline_until[user] > t means offline; using offline_until[user] <= t to check online.
  - Complexity: O(E log E) for sorting plus O(E * U) in worst case for processing (when using ALL/HERE), where E <= 100 and U <= 100. Space O(U) for offline tracking and result array.