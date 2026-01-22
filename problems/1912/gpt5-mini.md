# [Problem 1912: Design Movie Rental System](https://leetcode.com/problems/design-movie-rental-system/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need a system supporting search (cheapest 5 unrented shops for a movie), rent, drop, and report (cheapest 5 currently rented movies). Each entry is (shop, movie, price). We need efficient ordered access by price (and tie-breakers). Typical data structures: heaps sorted by (price, shop) per movie for available copies, and a global heap for rented copies sorted by (price, shop, movie). The challenge is deletions: rent/drop need to move items between available and rented sets; heaps don't support arbitrary deletions cheaply, so use lazy deletion (keep heaps and a set or dict to tell whether an entry is currently valid). When collecting top K we must avoid returning duplicates if heaps contain stale duplicates. Maintain quick mapping from (shop,movie) -> price. Also maintain sets: avail_set[movie] for currently unrented shops, and rented_set for currently rented (shop,movie) pairs. Use lazy-cleaning when peeking/popping from heaps and push popped items back to preserve heap state.

## Refining the problem, round 2 thoughts
Refinements and edge cases:
- Duplicate heap entries can accumulate (e.g., repeated drop pushes). When collecting top K we must ensure we don't return the same shop multiple times for a movie. Keep a `seen` set while gathering results.
- Use per-movie heap of (price, shop) for available copies, and a global rented heap of (price, shop, movie) for rented copies.
- Keep price_map[(shop,movie)] to know price quickly.
- Implement search(movie): fetch top up to 5 shops from the movie's available heap, skipping invalid entries (shop not in avail_set[movie]) and avoiding duplicates via seen.
- Implement rent(shop,movie): mark (shop,movie) as rented (add to rented_set), and push into rented_heap. Do not remove from available heap; lazy deletion will skip it later.
- Implement drop(shop,movie): remove from rented_set and add shop back into avail_set[movie], and push (price, shop) back into the available heap.
- Implement report(): get top up to 5 currently rented entries from rented_heap, skipping invalid entries (pairs not in rented_set), and avoid duplicates by tracking seen pairs. When gathering from heaps, pop entries into a temp list and push them back to restore original heaps (so operations are non-destructive).
- Complexity: each heap operation may lazy-pop invalid entries but total pops are amortized by number of pushes (<= number of operations). Each call will be efficient on average.

## Attempted solution(s)
```python
import heapq
from collections import defaultdict

class MovieRentingSystem:
    def __init__(self, n: int, entries: list[list[int]]):
        # price_map[(shop, movie)] = price
        self.price_map = {}
        # available heaps per movie: movie -> heap of (price, shop)
        self.avail_heaps = defaultdict(list)
        # set of currently available shops per movie (for validation & uniqueness)
        self.avail_set = defaultdict(set)
        # global rented heap of (price, shop, movie)
        self.rented_heap = []
        # set of currently rented pairs (shop, movie)
        self.rented_set = set()
        
        for shop, movie, price in entries:
            self.price_map[(shop, movie)] = price
            heapq.heappush(self.avail_heaps[movie], (price, shop))
            self.avail_set[movie].add(shop)

    def _top_k_available(self, movie: int, k: int):
        """Return up to k shops (ints) for given movie that are currently available,
        ordered by (price, shop). This does not modify availability; uses lazy pops
        and pushes popped elements back to preserve heaps."""
        res = []
        if movie not in self.avail_heaps:
            return res
        heap = self.avail_heaps[movie]
        temp = []
        seen_shops = set()
        # Pop until we've gathered k valid unique shops or heap exhausted
        while heap and len(res) < k:
            price, shop = heapq.heappop(heap)
            # If shop is currently available for this movie and we haven't added it yet
            if shop in self.avail_set[movie] and shop not in seen_shops:
                res.append(shop)
                seen_shops.add(shop)
            # push this popped entry to temp to restore later
            temp.append((price, shop))
        # push everything back to heap to preserve state
        for item in temp:
            heapq.heappush(heap, item)
        return res

    def _top_k_rented(self, k: int):
        """Return up to k [shop, movie] pairs currently rented, ordered by (price, shop, movie).
        Uses lazy popping and restores popped items."""
        res = []
        heap = self.rented_heap
        temp = []
        seen_pairs = set()
        while heap and len(res) < k:
            price, shop, movie = heapq.heappop(heap)
            pair = (shop, movie)
            if pair in self.rented_set and pair not in seen_pairs:
                res.append([shop, movie])
                seen_pairs.add(pair)
            temp.append((price, shop, movie))
        # restore heap
        for item in temp:
            heapq.heappush(heap, item)
        return res

    def search(self, movie: int) -> list[int]:
        # return up to 5 shops for movie that are currently available
        return self._top_k_available(movie, 5)

    def rent(self, shop: int, movie: int) -> None:
        # mark as rented and add to rented heap
        pair = (shop, movie)
        # it's guaranteed operation is valid (was unrented)
        if pair in self.rented_set:
            return
        self.rented_set.add(pair)
        # remove from avail_set (mark unrented)
        if shop in self.avail_set[movie]:
            self.avail_set[movie].remove(shop)
        price = self.price_map[(shop, movie)]
        heapq.heappush(self.rented_heap, (price, shop, movie))

    def drop(self, shop: int, movie: int) -> None:
        # mark as returned (no longer rented) and add back to available heap
        pair = (shop, movie)
        if pair in self.rented_set:
            self.rented_set.remove(pair)
        price = self.price_map[(shop, movie)]
        heapq.heappush(self.avail_heaps[movie], (price, shop))
        self.avail_set[movie].add(shop)

    def report(self) -> list[list[int]]:
        # return up to 5 currently rented pairs sorted by (price, shop, movie)
        return self._top_k_rented(5)
```
- Notes on approach:
  - We maintain per-movie min-heaps of available copies sorted by (price, shop). We also maintain a global min-heap of rented copies sorted by (price, shop, movie).
  - Because heaps don't support arbitrary deletes, use lazy deletion: keep sets to know what is currently available (avail_set[movie]) and what is currently rented (rented_set). When popping from heaps, skip entries that are no longer valid.
  - When collecting top K items for search/report we pop items into a temporary list and then push them back so the heap state remains unchanged.
  - Use seen sets while collecting so duplicates (caused by multiple pushes of identical tuples over time) do not appear multiple times in result.

- Complexity:
  - Initialization: O(E log E) for pushing entries (E = len(entries)).
  - search(movie): amortized O(k log E_movie) where k <= 5; lazy pops add extra work but total lazy pops across all operations is bounded by pushes (amortized).
  - rent/drop: O(log N) for heap push and O(1) for set operations (N is total entries).
  - report(): amortized O(k log R) where R is number of entries ever pushed into rented heap; k <= 5.
  - Space: O(E + number_of_operations) due to heaps and maps/sets.