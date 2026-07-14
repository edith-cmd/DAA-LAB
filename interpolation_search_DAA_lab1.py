"""
Interpolation Search vs Binary Search
======================================
An interactive command-line tool that lets the user:
  1. Enter their own sorted array (or auto-generate a random one)
  2. Search for a target value using Interpolation Search and/or Binary Search
  3. Run a performance benchmark comparing both algorithms across various sizes

Time Complexity:
  Interpolation Search -> O(log log n) average, O(n) worst case
  Binary Search        -> O(log n)

Space Complexity: O(1) for both

Author: (your name here)
"""

import time
import random


def interpolation_search(arr, target):
    """
    Interpolation Search Algorithm.
    Works best on uniformly distributed sorted arrays.

    Returns:
        (index, comparisons) -> index is -1 if not found
    """
    low, high = 0, len(arr) - 1
    comparisons = 0

    while low <= high and arr[low] <= target <= arr[high]:
        comparisons += 1

        if low == high:
            if arr[low] == target:
                return low, comparisons
            return -1, comparisons

        # Avoid division by zero if all values in range are equal
        if arr[high] == arr[low]:
            if arr[low] == target:
                return low, comparisons
            return -1, comparisons

        # Interpolation formula: estimate position based on target's value
        pos = low + int(((target - arr[low]) * (high - low)) / (arr[high] - arr[low]))

        if arr[pos] == target:
            return pos, comparisons
        elif arr[pos] < target:
            low = pos + 1
        else:
            high = pos - 1

    return -1, comparisons


def binary_search(arr, target):
    """Standard Binary Search for comparison."""
    low, high = 0, len(arr) - 1
    comparisons = 0

    while low <= high:
        comparisons += 1
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid, comparisons
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1, comparisons


# --------------------------------------------------------------------------
# Helper / input functions
# --------------------------------------------------------------------------

def get_user_array():
    """
    Prompts the user to either type their own sorted array or
    auto-generate a random sorted array of a chosen size.
    Returns a sorted list of integers.
    """
    print("\nHow would you like to provide the array?")
    print("  1. Enter numbers manually")
    print("  2. Auto-generate a random sorted array")
    choice = input("Choose an option (1/2): ").strip()

    if choice == "1":
        raw = input("Enter numbers separated by spaces or commas: ")
        raw = raw.replace(",", " ")
        try:
            arr = sorted(int(x) for x in raw.split())
        except ValueError:
            print("Invalid input detected. Please enter integers only.")
            return get_user_array()
        if not arr:
            print("Array cannot be empty. Please try again.")
            return get_user_array()
        return arr

    elif choice == "2":
        try:
            size = int(input("How many elements? (e.g. 20): ").strip())
            max_val = int(input("Maximum value in the array? (e.g. 200): ").strip())
        except ValueError:
            print("Please enter valid integers.")
            return get_user_array()

        if size <= 0 or max_val < size:
            print("Size must be positive and max value should be >= size.")
            return get_user_array()

        arr = sorted(random.sample(range(max_val), size))
        print(f"Generated array: {arr}")
        return arr

    else:
        print("Invalid choice, please try again.")
        return get_user_array()


def get_target(arr):
    """Prompts the user for a target value to search for."""
    while True:
        raw = input("\nEnter the target value to search for: ").strip()
        try:
            return int(raw)
        except ValueError:
            print("Please enter a valid integer.")


def run_single_search(arr, target):
    """Runs both search algorithms once and prints a readable result."""
    print(f"\nArray ({len(arr)} elements): {arr if len(arr) <= 30 else str(arr[:30]) + ' ...'}")
    print(f"Target: {target}")

    idx_is, comp_is = interpolation_search(arr, target)
    idx_bs, comp_bs = binary_search(arr, target)

    print("\n--- Results ---")
    if idx_is != -1:
        print(f"Interpolation Search: FOUND at index {idx_is} ({comp_is} comparisons)")
    else:
        print(f"Interpolation Search: NOT FOUND ({comp_is} comparisons)")

    if idx_bs != -1:
        print(f"Binary Search:        FOUND at index {idx_bs} ({comp_bs} comparisons)")
    else:
        print(f"Binary Search:        NOT FOUND ({comp_bs} comparisons)")


def performance_analysis(sizes=None):
    """
    Benchmarks Interpolation Search vs Binary Search across several array sizes.
    Uses randomly generated uniformly-distributed sorted arrays.
    """
    if sizes is None:
        raw = input(
            "\nEnter array sizes to benchmark, separated by spaces "
            "(press Enter for default 1000 5000 10000 50000 100000): "
        ).strip()
        if raw:
            try:
                sizes = [int(x) for x in raw.split()]
            except ValueError:
                print("Invalid input, using default sizes.")
                sizes = [1000, 5000, 10000, 50000, 100000]
        else:
            sizes = [1000, 5000, 10000, 50000, 100000]

    print()
    print(f"{'Size':>10} {'IS Time(ms)':>14} {'BS Time(ms)':>14} "
          f"{'IS Comparisons':>16} {'BS Comparisons':>16}")
    print('-' * 75)

    for size in sizes:
        arr = sorted(random.sample(range(size * 10), size))
        target = arr[random.randint(0, size - 1)]

        # Interpolation Search timing
        start = time.perf_counter()
        for _ in range(100):
            idx_is, comp_is = interpolation_search(arr, target)
        is_time = (time.perf_counter() - start) / 100 * 1000

        # Binary Search timing
        start = time.perf_counter()
        for _ in range(100):
            idx_bs, comp_bs = binary_search(arr, target)
        bs_time = (time.perf_counter() - start) / 100 * 1000

        print(f"{size:>10} {is_time:>14.4f} {bs_time:>14.4f} "
              f"{comp_is:>16} {comp_bs:>16}")


# --------------------------------------------------------------------------
# Main menu
# --------------------------------------------------------------------------

def main():
    print("=" * 60)
    print(" Interpolation Search vs Binary Search - Interactive Demo")
    print("=" * 60)

    while True:
        print("\nMain Menu:")
        print("  1. Search in a custom/random array")
        print("  2. Run performance benchmark")
        print("  3. Exit")
        choice = input("Choose an option (1/2/3): ").strip()

        if choice == "1":
            arr = get_user_array()
            target = get_target(arr)
            run_single_search(arr, target)

        elif choice == "2":
            performance_analysis()

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
