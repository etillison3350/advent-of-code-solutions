from __future__ import annotations
from typing import Sequence

import input


class LinkedListNode:
    data: int
    next: LinkedListNode

    def __init__(self, data: int, next_node: LinkedListNode = None):
        self.data = data
        self.next = next_node

    def set_next(self, next_node):
        self.next = next_node


def crab_game(cups: Sequence[int], num_iterations: int) -> LinkedListNode:
    max_cup_value = max(cups)

    # Store the cups as a circularly linked list
    head = LinkedListNode(cups[0])
    curr_node = head
    for cup in cups[1:]:
        new_node = LinkedListNode(cup)
        curr_node.set_next(new_node)
        curr_node = new_node
    curr_node.set_next(head)

    # Instead of applying updates to the linked list immediately (since this requires an O(n) search), store the updates
    # that are going to be made, and apply the updates only when they would affect the output
    updates = {}

    curr_node = head
    for _ in range(num_iterations):
        # Apply updates to the current node and the three subsequent nodes
        update_node = curr_node
        for _ in range(4):
            if update_node.data in updates:
                updates[update_node.data].next.next.set_next(update_node.next)
                update_node.set_next(updates[update_node.data])
                del updates[update_node.data]
            update_node = update_node.next

        # Remove the three nodes following the current one
        curr_cup = curr_node.data
        remove_node = curr_node.next
        curr_node.set_next(curr_node.next.next.next.next)

        # Compute the target value; this is the greatest valued cup less than the value of the current cup (or just the
        # greatest value, if no such cup exists), excluding the cups just removed
        target_value = (curr_cup - 2) % max_cup_value + 1
        while target_value in [remove_node.data, remove_node.next.data, remove_node.next.next.data]:
            target_value = (target_value - 2) % max_cup_value + 1
        updates[target_value] = remove_node

        curr_node = curr_node.next

    # Apply all updates that haven't been applied yet. Since we're really only concerned about the few values after 1,
    # we could be a little bit more efficient here, but this isn't too expensive an operation
    while len(updates):
        if curr_node.data in updates:
            updates[curr_node.data].next.next.set_next(curr_node.next)
            curr_node.set_next(updates[curr_node.data])
            del updates[curr_node.data]
        curr_node = curr_node.next

    # Find the node with data 1 and return it
    while curr_node.data != 1:
        curr_node = curr_node.next
    return curr_node


def run(r: Sequence[str]):
    # Part 1
    cups = [int(k) for k in r[0]]
    cup_list = []
    start_node = crab_game(cups, 100)
    curr_node = start_node.next
    while curr_node != start_node:
        cup_list.append(curr_node.data)
        curr_node = curr_node.next
    print(''.join(str(k) for k in cup_list))

    # Part 2
    cups = cups + list(range(max(cups) + 1, 1000001))
    curr_node = crab_game(cups, 10000000).next
    print(curr_node.data * curr_node.next.data)


if __name__ == '__main__':
    day, year = 23, 2020
    input.wait_for_input(day, year)

    split_seq = '\n'

    inp = input.input_text(day, year)
    input_lines = inp.split(split_seq)

    print('True output:')
    run(input_lines)
    print()

    print('Possible test cases:')
    test_cases = input.find_test_cases(day, year, cached=True)
    for index, tc in enumerate(test_cases):
        tc_list = tc.split(split_seq)
        tc_str = str(tc_list)
        print('Test case {}: {}{}'.format(index, tc_str[:80], '...' if len(tc_str) > 80 else ''))
        try:
            run(tc_list)
        except Exception as ex:
            print('{}: {}'.format(type(ex).__name__, ex))
        finally:
            print('Done with test case {}'.format(index))
