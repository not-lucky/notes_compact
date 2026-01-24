class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverseList(head: ListNode) -> ListNode:
    prev = None
    curr = head
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    return prev

def test_reverse_list():
    # Helper to convert list to linked list
    def to_linked_list(arr):
        if not arr: return None
        head = ListNode(arr[0])
        curr = head
        for val in arr[1:]:
            curr.next = ListNode(val)
            curr = curr.next
        return head

    # Helper to convert linked list to list
    def to_list(node):
        arr = []
        while node:
            arr.append(node.val)
            node = node.next
        return arr

    head = to_linked_list([1,2,3,4,5])
    reversed_head = reverseList(head)
    assert to_list(reversed_head) == [5,4,3,2,1]

    head = to_linked_list([1,2])
    reversed_head = reverseList(head)
    assert to_list(reversed_head) == [2,1]

    head = to_linked_list([])
    reversed_head = reverseList(head)
    assert to_list(reversed_head) == []

    print("Reverse Linked List tests passed!")

if __name__ == "__main__":
    test_reverse_list()
