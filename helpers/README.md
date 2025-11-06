# LeetCode Helper Functions

This folder contains utility functions and data structures to help with debugging and solving LeetCode problems.

## 📚 Contents

- **[data_structures.py](data_structures.py)**: Common data structures (TreeNode, ListNode)
- **[tree_utils.py](tree_utils.py)**: Binary tree helper functions
- **[linked_list_utils.py](linked_list_utils.py)**: Linked list helper functions
- **[algorithms.py](algorithms.py)**: Common algorithms (BFS, DFS, tree search)

## 🚀 Demo Notebooks

Interactive Jupyter notebooks demonstrating the helper functions:

- **[Binary Trees Demo](demo_binary_trees.ipynb)** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ContextLab/leetcode-solutions/blob/main/helpers/demo_binary_trees.ipynb)
- **[Linked Lists Demo](demo_linked_lists.ipynb)** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ContextLab/leetcode-solutions/blob/main/helpers/demo_linked_lists.ipynb)

## 📖 Quick Start

### Installation

From the root of the repository:

```python
from helpers import *
```

### Binary Trees

#### Creating Trees

```python
from helpers import list_to_tree, print_tree

# Create a tree from a list (LeetCode format)
tree = list_to_tree([1, 2, 3, 4, 5, None, 7])

# Visualize it
print_tree(tree)
# Output:
# Root: 1
# ├─ L: 2
# │  ├─ L: 4
# │  └─ R: 5
# └─ R: 3
#    └─ R: 7
```

#### Converting Trees

```python
from helpers import tree_to_list

# Convert a tree back to a list
tree_list = tree_to_list(tree)
print(tree_list)  # [1, 2, 3, 4, 5, None, 7]
```

#### Tree Traversals

```python
from helpers import bfs_traversal, dfs_preorder, dfs_inorder, dfs_postorder

tree = list_to_tree([1, 2, 3, 4, 5])

print(bfs_traversal(tree))    # [1, 2, 3, 4, 5]
print(dfs_preorder(tree))     # [1, 2, 4, 5, 3]
print(dfs_inorder(tree))      # [4, 2, 5, 1, 3]
print(dfs_postorder(tree))    # [4, 5, 2, 3, 1]
```

### Linked Lists

#### Creating Linked Lists

```python
from helpers import list_to_linked_list, print_linked_list

# Create a linked list from a Python list
head = list_to_linked_list([1, 2, 3, 4, 5])

# Visualize it
print_linked_list(head)
# Output: 1 -> 2 -> 3 -> 4 -> 5 -> None
```

#### Converting Linked Lists

```python
from helpers import linked_list_to_list

# Convert back to a Python list
result = linked_list_to_list(head)
print(result)  # [1, 2, 3, 4, 5]
```

#### Accessing Nodes

```python
from helpers import get_node_at_index, get_linked_list_length

head = list_to_linked_list([10, 20, 30, 40, 50])

# Get length
length = get_linked_list_length(head)  # 5

# Get node at index
node = get_node_at_index(head, 2)
print(node.val)  # 30
```

## 📋 Complete Function Reference

### Data Structures

#### TreeNode
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None)
```
Standard binary tree node used in LeetCode problems.

#### ListNode
```python
class ListNode:
    def __init__(self, val=0, next=None)
```
Standard linked list node used in LeetCode problems.

### Binary Tree Functions

#### Conversion Functions
- `list_to_tree(values)`: Convert a list to a binary tree (level-order)
- `tree_to_list(root)`: Convert a binary tree to a list (level-order)

#### Visualization Functions
- `print_tree(root)`: Print a visual representation of a tree
- `visualize_tree(root)`: Get a string representation of a tree

#### Tree Properties
- `get_tree_height(root)`: Get the height of a tree
- `count_nodes(root)`: Count total nodes in a tree

### Linked List Functions

#### Conversion Functions
- `list_to_linked_list(values)`: Convert a Python list to a linked list
- `linked_list_to_list(head)`: Convert a linked list to a Python list

#### Visualization Functions
- `print_linked_list(head)`: Print a visual representation of a linked list

#### List Properties
- `get_linked_list_length(head)`: Get the length of a linked list
- `get_node_at_index(head, index)`: Get the node at a specific index

### Algorithm Functions

#### Tree Traversals
- `bfs_traversal(root)`: Breadth-first search (level-order) traversal
- `dfs_preorder(root)`: Depth-first search pre-order traversal
- `dfs_inorder(root)`: Depth-first search in-order traversal
- `dfs_postorder(root)`: Depth-first search post-order traversal
- `level_order_traversal(root)`: Level-order traversal grouped by level

#### Tree Search
- `find_path_to_node(root, target)`: Find path from root to a target node
- `lowest_common_ancestor(root, p, q)`: Find the lowest common ancestor of two nodes
- `search_bst(root, target)`: Search for a value in a Binary Search Tree
- `is_valid_bst(root)`: Check if a tree is a valid Binary Search Tree

## 💡 Usage Examples

### Example 1: Testing Your Solution

```python
from helpers import list_to_tree, tree_to_list

def your_solution(root):
    # Your solution code here
    pass

# Test with LeetCode test case
test_input = [1, 2, 3, 4, 5, None, 7]
tree = list_to_tree(test_input)
result = your_solution(tree)
print(tree_to_list(result))
```

### Example 2: Debugging Tree Structure

```python
from helpers import list_to_tree, print_tree, get_tree_height, count_nodes

tree = list_to_tree([1, 2, 3, 4, 5, 6, 7, 8])

print("Tree structure:")
print_tree(tree)

print(f"\nHeight: {get_tree_height(tree)}")
print(f"Total nodes: {count_nodes(tree)}")
```

### Example 3: Visualizing Linked List Operations

```python
from helpers import list_to_linked_list, print_linked_list

# Before operation
head = list_to_linked_list([1, 2, 3, 4, 5])
print("Before:")
print_linked_list(head)

# Your operation here (e.g., reverse)
# ...

print("\nAfter:")
print_linked_list(head)
```

### Example 4: Understanding Tree Traversals

```python
from helpers import list_to_tree, print_tree
from helpers import bfs_traversal, dfs_preorder, dfs_inorder, dfs_postorder

tree = list_to_tree([1, 2, 3, 4, 5, 6, 7])

print("Tree:")
print_tree(tree)
print()

print("Traversals:")
print(f"BFS:        {bfs_traversal(tree)}")
print(f"Pre-order:  {dfs_preorder(tree)}")
print(f"In-order:   {dfs_inorder(tree)}")
print(f"Post-order: {dfs_postorder(tree)}")
```

## 🤝 Contributing

Feel free to add more helper functions as you encounter common patterns in LeetCode problems!

To add a new helper:
1. Add the function to the appropriate module (`tree_utils.py`, `linked_list_utils.py`, etc.)
2. Update `__init__.py` to export the function
3. Add documentation and examples
4. Update this README

## 📝 Notes

- All functions follow LeetCode's standard conventions for data structures
- `None` in tree lists represents null nodes (LeetCode format)
- Functions are designed to be copy-paste friendly for LeetCode submissions
- Visualization functions are great for debugging but won't work on LeetCode (they don't affect solutions)

## 🔗 Related Resources

- [LeetCode Official Site](https://leetcode.com)
- [Main Repository README](../README.md)
- [Problems We've Solved](../problems)

Happy coding! 🎉
