import sys
from functools import reduce

def read_ints_from_line(line):
    """
    Convert a line of space-separated numbers into a list of ints.
    Example: "3 -1 1 10" -> [3, -1, 1, 10]
    """
    return list(map(int, line.strip().split())) if line.strip() else []

def sum_negative_fourth_powers(nums):
    """
    Take only the negative numbers from nums,
    raise them to the 4th power, and return the sum.
    Example: [3, -1, 1, 10] -> (-1)^4 = 1
    """
    negatives = list(filter(lambda x: x < 0, nums))
    return reduce(lambda acc, y: acc + (y ** 4), negatives, 0)

def process_case(case_lines):
    """
    Process a single test case.
    case_lines is a list with two elements:
        [0] -> the integer X (count of expected numbers)
        [1] -> the line containing the numbers
    If the number of provided integers != X, return -1.
    Otherwise, return the sum of 4th powers of negatives.
    """
    if len(case_lines) < 2:
        return -1
    try:
        x = int(case_lines[0].strip())
        nums = read_ints_from_line(case_lines[1])
    except Exception:
        return -1

    if len(nums) != x:
        return -1
    return sum_negative_fourth_powers(nums)

def recursive_process(cases, idx=0, acc=None):
    """
    Recursively process all test cases.
    No loops allowed, so we move through the list with recursion.
    """
    if acc is None:
        acc = []
    if idx >= len(cases):
        return acc
    result = process_case(cases[idx])
    acc.append(result)
    return recursive_process(cases, idx + 1, acc)

def group_lines(lines, n):
    """
    Split the raw input lines into groups of two (per test case).
    Example: n=2, lines=[4, "3 -1 1 10", 5, "9 -5 -5 -10 10"]
    -> [[[4], ["3 -1 1 10"]], [[5], ["9 -5 -5 -10 10"]]]
    """
    def helper(lines, n, acc=None):
        if acc is None:
            acc = []
        if not lines or n == 0:
            return acc
        case = lines[:2]   # first two lines = one test case
        rest = lines[2:]   # remaining lines
        acc.append(case)
        return helper(rest, n - 1, acc)
    return helper(lines, n)

def main():
    # Read all input at once
    data = sys.stdin.read().splitlines()
    if not data:
        return
    try:
        # First line = number of test cases
        t = int(data[0].strip())
    except Exception:
        return
    # Group the following lines into test cases
    cases = group_lines(data[1:], t)
    # Process test cases recursively
    results = recursive_process(cases)
    # Print results line by line (no blank lines in between)
    sys.stdout.write("\n".join(map(str, results)))

if __name__ == "__main__":
    main()
