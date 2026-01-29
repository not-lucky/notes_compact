# Chapter 15: Bit Manipulation Solutions

This directory contains optimal Python solutions for the practice problems found in the Bit Manipulation chapter. Bit manipulation is a powerful tool in competitive programming and technical interviews, allowing for highly efficient O(1) space and time complexity for many operations.

## Topic Hierarchy

| Section | Topic                                                      | Key Concepts                                          |
| ------- | ---------------------------------------------------------- | ----------------------------------------------------- |
| 01      | [Binary Basics](./01-binary-basics.md)                     | String addition, bit flipping, linked list conversion |
| 02      | [Single Number](./02-single-number.md)                     | XOR properties, state machines, cycle detection       |
| 03      | [Counting Bits](./03-counting-bits.md)                     | Brian Kernighan's, DP, per-bit counting               |
| 04      | [Power of Two](./04-power-of-two.md)                       | Bit patterns, range AND, highest set bit              |
| 05      | [XOR Tricks](./05-xor-tricks.md)                           | Missing number, prefix XOR, max XOR with prefixes     |
| 06      | [Bit Manipulation Tricks](./06-bit-manipulation-tricks.md) | Subsets, Gray code, UTF-8 validation                  |

## Core Principles

The solutions in this directory prioritize:

1. **Optimal Time Complexity**: Leveraging bitwise operators for constant or linear time solutions.
2. **Minimal Space Complexity**: Using O(1) extra space whenever possible, which is the hallmark of bit manipulation.
3. **Clarity**: Detailed explanations for why specific bitwise formulas work.

## Essential Bitwise Formulas

| Goal                      | Formula                        | Logic                                                |
| ------------------------- | ------------------------------ | ---------------------------------------------------- |
| Clear rightmost set bit   | `n & (n - 1)`                  | Flips rightmost 1 to 0 and all 0s to its right to 1. |
| Isolate rightmost set bit | `n & -n`                       | Uses two's complement property.                      |
| Check power of 2          | `n > 0 and (n & (n - 1)) == 0` | Powers of 2 have exactly one bit set.                |
| Swap without temp         | `a ^= b; b ^= a; a ^= b`       | XOR properties `a^a=0` and `a^0=a`.                  |
| Add bits without carry    | `a ^ b`                        | Sum of binary digits mod 2.                          |
| Find carry bits           | `(a & b) << 1`                 | Carry occurs only if both bits are 1.                |

## How to Use These Solutions

Each markdown file corresponds to a specific subtopic. For every problem, you will find:

- **Problem Statement**: A clear description of the task.
- **Examples**: Illustrative cases including edge cases.
- **Optimal Implementation**: Clean, commented Python code.
- **Step-by-step Explanation**: Breakdown of the logic and bitwise properties used.
- **Complexity Analysis**: Formal Big-O notation for time and space.
