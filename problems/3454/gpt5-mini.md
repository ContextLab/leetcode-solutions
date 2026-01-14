# [Problem 3454: Separate Squares II](https://leetcode.com/problems/separate-squares-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the minimal horizontal line y = c such that the total union area of all squares above the line equals the total union area below the line. Counting union area (overlaps only once) is the key difficulty.

A brute-force idea: for any candidate c, clip every square by y <= c and compute union area of resulting rectangles; binary search c to find when clipped area equals half. But computing union area per query naively (sweep-line + segment tree) would be expensive when repeated many times.

Observation: if we consider the function A(c) = area below line y = c (union area of squares clipped at top c), A(c) is non-decreasing and in fact piecewise-linear. Its slope at y is the union length of x-projections of squares that cover that horizontal y. The slope changes only at square bottoms y_i and tops y_i + l_i. So we can sweep y across these event coordinates once, maintain the current union x-length with a segment tree, and accumulate area slab-by-slab. That gives the entire union area as well as a piecewise-linear representation so we can compute the exact c where A(c) = T/2.

Thus do a single sweep over y with add/remove events for each square's x-intervals, maintain covered x-length, accumulate area across slabs between consecutive y events; when accumulated area crosses T/2 within a slab, compute c by simple linear interpolation.

## Refining the problem, round 2 thoughts
Details to handle:
- Build events: (y, +1, x, x+l) for square bottom, (y+l, -1, x, x+l) for top.
- Sort events by y. For each distinct y_k, apply all events at y_k (so intervals starting at y_k are active on the slab above y_k), then the covered x-length applies to the slab [y_k, y_{k+1}).
- Maintain union length of many x-intervals under dynamic add/remove; classic segment tree over compressed x-coordinates with coverage counts and covered length.
- Track accumulated area; total union area T will be the final accumulation. Target = T/2. During sweep, if target lies in the current slab, covered length L > 0 (otherwise area doesn't change), then c = y_k + (target - area_before)/L. If L == 0 and target == area_before then minimal c is y_k.
- Complexity: sorting events O(n log n). Each update on segment tree is O(log m) where m = number of unique x endpoints (<= 2n). We do 2n updates -> O(n log n). Memory O(n).

Edge cases:
- Several events share the same y; process all together.
- Target might be exactly at some event y; minimal c should be that event y.
- Large coordinates up to 1e9, area up to 1e15 -> use float (double) for final value; intermediate covered lengths also large but fit in float/double; use Python float.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def separateSquares(self, squares: List[List[int]]) -> float:
        # Build events and x-coordinates
        events = []  # (y, typ, x_left, x_right) typ = +1 add, -1 remove
        xs = []
        for x, y, l in squares:
            xl = x
            xr = x + l
            yb = y
            yt = y + l
            events.append((yb, 1, xl, xr))
            events.append((yt, -1, xl, xr))
            xs.append(xl)
            xs.append(xr)
        if not events:
            return 0.0

        events.sort(key=lambda e: e[0])
        xs = sorted(set(xs))
        # map x -> index
        xi = {v:i for i, v in enumerate(xs)}
        m = len(xs)
        if m < 2:
            # no horizontal span
            return float(events[0][0])

        # Segment tree over elementary segments between xs[i] and xs[i+1], indices [0..m-2]
        seg_len = [0.0] * (4 * (m-1))
        seg_count = [0] * (4 * (m-1))

        def update(node, l, r, ql, qr, val):
            # node covers [l, r] inclusive in terms of segment indices (0..m-2)
            if ql > r or qr < l:
                return
            if ql <= l and r <= qr:
                seg_count[node] += val
            else:
                mid = (l + r) // 2
                update(node*2, l, mid, ql, qr, val)
                update(node*2+1, mid+1, r, ql, qr, val)
            # compute covered length for this node
            if seg_count[node] > 0:
                # fully covered
                seg_len[node] = xs[r+1] - xs[l]
            else:
                if l == r:
                    seg_len[node] = 0.0
                else:
                    seg_len[node] = seg_len[node*2] + seg_len[node*2+1]

        total_area = 0.0
        target = None  # will be set after computing total_area, but we can compute on the fly too
        # We'll do a single sweep and look for when cumulative area reaches T/2.
        # First pass: sweep once but we need T to compute target. We can either do full sweep to get T then second sweep to find position,
        # but we can detect crossing in the same sweep if we know T/2 in advance. So first compute total union area T by sweeping.
        # We'll reuse same structure; do first pass to compute T.
        # Reset tree arrays (they are already zero)
        idx = 0
        n_events = len(events)
        total_area = 0.0
        while idx < n_events:
            y = events[idx][0]
            # process all events at y
            while idx < n_events and events[idx][0] == y:
                _, typ, xl, xr = events[idx]
                lidx = xi[xl]
                ridx = xi[xr]
                if lidx < ridx:
                    update(1, 0, m-2, lidx, ridx-1, typ)
                idx += 1
            # next y
            if idx >= n_events:
                break
            next_y = events[idx][0]
            covered_x = seg_len[1]
            dy = next_y - y
            if covered_x > 0 and dy > 0:
                total_area += covered_x * dy
        # Now we have total_area T
        target = total_area / 2.0

        # If target is 0 -> minimal y is minimal y where area stays 0 i.e., minimal event y
        if target == 0.0:
            # find minimal y where below area is zero minimal => it's smallest event y
            return float(events[0][0])

        # Reset segment tree and sweep again to find exact c
        seg_len = [0.0] * (4 * (m-1))
        seg_count = [0] * (4 * (m-1))
        def update2(node, l, r, ql, qr, val):
            if ql > r or qr < l:
                return
            if ql <= l and r <= qr:
                seg_count[node] += val
            else:
                mid = (l + r) // 2
                update2(node*2, l, mid, ql, qr, val)
                update2(node*2+1, mid+1, r, ql, qr, val)
            if seg_count[node] > 0:
                seg_len[node] = xs[r+1] - xs[l]
            else:
                if l == r:
                    seg_len[node] = 0.0
                else:
                    seg_len[node] = seg_len[node*2] + seg_len[node*2+1]

        cum_area = 0.0
        idx = 0
        while idx < n_events:
            y = events[idx][0]
            # process all events at this y
            while idx < n_events and events[idx][0] == y:
                _, typ, xl, xr = events[idx]
                lidx = xi[xl]
                ridx = xi[xr]
                if lidx < ridx:
                    update2(1, 0, m-2, lidx, ridx-1, typ)
                idx += 1
            if idx >= n_events:
                break
            next_y = events[idx][0]
            covered_x = seg_len[1]
            dy = next_y - y
            area_before = cum_area
            area_after = area_before + covered_x * dy
            # Check if target lies in [area_before, area_after]
            if target >= area_before and target <= area_after:
                if covered_x == 0.0:
                    # area not changing in this slab; minimal y is y
                    return float(y)
                # linear interpolation within slab
                need = target - area_before
                c = y + need / covered_x
                return float(c)
            cum_area = area_after
        # If not found in sweep (possible due to numerical issues), return topmost y
        # topmost y is max(y_i + l_i)
        topmost = max(y + l for (_, y, l) in squares)
        return float(topmost)
```
- Approach notes:
  - We perform a sweep over y events (square bottoms and tops). At each y, we apply add/remove updates of the squares' x-intervals to a segment tree that maintains the union length of active x-intervals.
  - For each slab between consecutive y-coordinates, the union x-length is constant, so the area contributed is covered_x * dy. We accumulate area and check when we cross T/2 and compute the exact c by linear interpolation inside the slab.
  - Time complexity: O(n log n) due to sorting and O(n) segment-tree updates each costing O(log n) over compressed x coordinates.
  - Space complexity: O(n) for events, coordinate arrays, and segment tree.
  - Implementation details: we compress x endpoints, maintain segment tree over m-1 elementary x-segments with coverage counts; when a node's count > 0 its covered length equals the node's x-span, else it's sum of childrens' covered lengths. We sweep twice: once to compute total area T, then again to locate the slab containing T/2 and compute exact y. (Could be merged but two sweeps keep logic clear.)