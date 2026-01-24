class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def has_cycle(head: ListNode) -> bool:
    """
    Determine if a linked list has a cycle.
    Pattern: Fast/Slow Pointers
    Time: O(n)
    Space: O(1)
    """
    if not head or not head.next:
        return False

    slow = head
    fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow == fast:
            return True

    return False

if __name__ == "__main__":
    # Test cases
    # Case 1: Cycle
    node1 = ListNode(3)
    node2 = ListNode(2)
    node3 = ListNode(0)
    node4 = ListNode(-4)
    node1.next = node2
    node2.next = node3
    node3.next = node4
    node4.next = node2
    assert has_cycle(node1) == True

    # Case 2: No cycle
    nodeA = ListNode(1)
    nodeB = ListNode(2)
    nodeA.next = nodeB
    assert has_cycle(nodeA) == False

    # Case 3: Single node no cycle
    assert has_cycle(ListNode(1)) == False

    print("All tests passed!")
