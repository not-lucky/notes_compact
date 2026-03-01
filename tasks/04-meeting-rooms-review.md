# Meeting Rooms Improvements

I have analyzed and improved `12-greedy/04-meeting-rooms.md`. Here is a summary of the improvements made:

1.  **Code Readability and Correctness**:
    *   Checked that all existing python3 code snippets correctly solve the problems and use standard `list[list[int]]` typing.
    *   Refined the python syntax in `can_attend_meetings` and explicitly clarified that `sorted` in python takes `O(n)` memory because it creates a new list, unlike C++ `std::sort`.

2.  **Practice Problems Evolution**:
    *   Replaced the "Find Right Interval" (LC 436) problem with the "My Calendar I and II" (LC 729, 731) problems. "Find Right Interval" is fundamentally a binary search problem and doesn't fit the "tracking active intervals" theme of this file.
    *   The "My Calendar" series dynamically handles adding intervals while tracking active overlaps. They directly teach how to build a sweep line tracking overlap on the fly, which builds upon "Meeting Rooms I & II" wonderfully.

3.  **Complexity Table Updates**:
    *   Updated the complexity table at the bottom of the document to reflect the changes to the practice problems and to fix the space complexity for Meeting Rooms I to `O(n)` to reflect python's `sorted()` memory footprint (not `O(1)` as previously stated).

4.  **Verification**:
    *   I wrote local test scripts for every single code block in the file to run the code and verify its correctness against edge cases, ensuring that no flawed logic was committed. The tests successfully passed.

The document is now cleaner, the progression makes much more conceptual sense, and the code examples are verified.