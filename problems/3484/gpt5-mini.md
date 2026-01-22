# [Problem 3484: Design Spreadsheet](https://leetcode.com/problems/design-spreadsheet/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The problem describes a simple spreadsheet with 26 columns (A..Z) and a number of rows. We need to support setCell, resetCell, and evaluating formulas of the form "=X+Y" where X and Y are either integers or cell references. There is no requirement to store formulas in cells or propagate dependencies — setCell stores a concrete integer for a single cell and getValue just computes a sum possibly looking up cell values. So a straightforward mapping from cell identifier to integer value should suffice.

Parsing: formulas always start with '=' and contain exactly one '+' separating two operands. Each operand is either a non-negative integer (string of digits) or a cell reference (one capital letter A-Z followed by digits for the row). For cell references not explicitly set, value is 0.

So the plan: keep a dictionary mapping cell keys (e.g., "A1") to integers. setCell stores value, resetCell removes the key (or sets to 0). getValue parses the formula, for each operand if .isdigit() -> int else look up dict.get(operand, 0) and sum.

This should be O(1) work per operation (string parsing and dict lookup).

## Refining the problem, round 2 thoughts
Edge cases to consider:
- Operands with multiple digits (like "100") — .isdigit() handles that.
- Leading zeros (like "005") — int() handles that and values remain valid.
- A cell that was never set or was reset should be treated as 0 -> use dict.get(key, 0).
- Rows are 1-indexed in input but we don't need numeric indices other than as part of the key string, so storing the original "A1" string is fine.
- Input guarantees valid formats; no need for heavy validation.
Alternative: store keys as (col_index, row_index) tuples, but storing the original string is simpler and efficient here.
Time/space: Each operation is O(1) average time (dict operations) and O(k) extra space where k is number of set cells.

## Attempted solution(s)
```python
class Spreadsheet:
    def __init__(self, rows: int):
        """
        Initialize spreadsheet with given rows and 26 columns (A..Z).
        We'll store only explicitly set cells in a dictionary mapping
        the cell string like "A1" -> int value. Unset cells are treated as 0.
        """
        self.rows = rows
        self.cells = {}  # maps cell string "A1" -> int

    def setCell(self, cell: str, value: int) -> None:
        # store the explicit value for the cell
        self.cells[cell] = value

    def resetCell(self, cell: str) -> None:
        # reset to 0 by removing from the dict if present
        if cell in self.cells:
            del self.cells[cell]

    def getValue(self, formula: str) -> int:
        # formula format guaranteed: "=X+Y" where X and Y are either numbers or cell refs
        # strip leading '=' and split by '+'
        assert formula and formula[0] == '='
        expr = formula[1:]
        left, right = expr.split('+', 1)

        def operand_value(token: str) -> int:
            # if token is numeric (digits only) -> parse as int, else look up cell
            if token.isdigit():
                return int(token)
            return self.cells.get(token, 0)

        return operand_value(left) + operand_value(right)
```
- Approach notes: Use a dictionary to store only explicitly set cells. getValue parses the formula into two operands; numeric operands are converted with int(), cell operands are looked up in the dict with default 0.
- Time complexity: O(1) average per operation (dict lookups and small string parsing). Splitting and isdigit are O(L) in the length of the formula where L is small (bounded).
- Space complexity: O(k) where k is the number of cells that have been set (stored in the dict).