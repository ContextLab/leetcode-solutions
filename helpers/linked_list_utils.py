"""
Utility functions for working with linked lists.
"""

from typing import Optional, List
from .data_structures import ListNode


def list_to_linked_list(values: List[int]) -> Optional[ListNode]:
    """
    Convert a Python list to a singly-linked list.
    
    Args:
        values: List of values to convert
        
    Returns:
        Head node of the created linked list, or None if input is empty
        
    Example:
        >>> head = list_to_linked_list([1, 2, 3, 4, 5])
        >>> # Creates: 1 -> 2 -> 3 -> 4 -> 5
    """
    if not values:
        return None
    
    head = ListNode(values[0])
    current = head
    
    for val in values[1:]:
        current.next = ListNode(val)
        current = current.next
    
    return head


def linked_list_to_list(head: Optional[ListNode]) -> List[int]:
    """
    Convert a singly-linked list to a Python list.
    
    Args:
        head: Head node of the linked list
        
    Returns:
        List of values from the linked list
        
    Example:
        >>> head = ListNode(1)
        >>> head.next = ListNode(2)
        >>> head.next.next = ListNode(3)
        >>> linked_list_to_list(head)
        [1, 2, 3]
    """
    result = []
    current = head
    
    while current:
        result.append(current.val)
        current = current.next
    
    return result


def print_linked_list(head: Optional[ListNode]) -> None:
    """
    Print a visual representation of a linked list.
    
    Args:
        head: Head node of the linked list
        
    Example:
        >>> head = list_to_linked_list([1, 2, 3, 4])
        >>> print_linked_list(head)
        1 -> 2 -> 3 -> 4 -> None
    """
    if not head:
        print("Empty list")
        return
    
    values = linked_list_to_list(head)
    print(" -> ".join(map(str, values)) + " -> None")


def get_linked_list_length(head: Optional[ListNode]) -> int:
    """
    Calculate the length of a linked list.
    
    Args:
        head: Head node of the linked list
        
    Returns:
        Number of nodes in the linked list
        
    Example:
        >>> head = list_to_linked_list([1, 2, 3, 4, 5])
        >>> get_linked_list_length(head)
        5
    """
    length = 0
    current = head
    
    while current:
        length += 1
        current = current.next
    
    return length


def get_node_at_index(head: Optional[ListNode], index: int) -> Optional[ListNode]:
    """
    Get the node at a specific index in the linked list.
    
    Args:
        head: Head node of the linked list
        index: Zero-based index of the node to retrieve
        
    Returns:
        Node at the specified index, or None if index is out of bounds
        
    Example:
        >>> head = list_to_linked_list([1, 2, 3, 4, 5])
        >>> node = get_node_at_index(head, 2)
        >>> node.val
        3
    """
    current = head
    current_index = 0
    
    while current and current_index < index:
        current = current.next
        current_index += 1
    
    return current
