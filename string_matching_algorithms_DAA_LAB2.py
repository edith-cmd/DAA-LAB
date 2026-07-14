"""
String Matching Algorithms: Naive vs KMP vs Rabin-Karp
========================================================
An interactive command-line tool that lets the user:
  1. Enter their own text and pattern (or auto-generate random ones)
  2. Search for the pattern using Naive Search, KMP, and Rabin-Karp
  3. Run a performance benchmark comparing all three algorithms
     across multiple patterns on a large randomly generated text

Time Complexity:
  Naive Search  -> O((n - m + 1) * m) worst case
  KMP           -> O(n + m)
  Rabin-Karp    -> O(n + m) average, O(n * m) worst case

Space Complexity:
  Naive Search  -> O(1)
  KMP           -> O(m)   (for the LPS array)
  Rabin-Karp    -> O(1)

Author: (your name here)
"""

import random
import string


def naive_search(text, pattern):
    """Naive (brute-force) pattern search."""
    n, m = len(text), len(pattern)
    matches, comparisons = [], 0

    for i in range(n - m + 1):
        j = 0
        while j < m:
            comparisons += 1
            if text[i + j] != pattern[j]:
                break
            j += 1
        if j == m:
            matches.append(i)

    return matches, comparisons


def compute_lps(pattern):
    """Computes the Longest Prefix Suffix (LPS) array used by KMP."""
    m = len(pattern)
    lps = [0] * m
    length, i = 0, 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1

    return lps


def kmp_search(text, pattern):
    """Knuth-Morris-Pratt pattern search."""
    n, m = len(text), len(pattern)
    lps = compute_lps(pattern)
    matches, comparisons = [], 0
    i = j = 0

    while i < n:
        comparisons += 1
        if pattern[j] == text[i]:
            i += 1
            j += 1
            if j == m:
                matches.append(i - j)
                j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return matches, comparisons


def rabin_karp(text, pattern, q=101):
    """Rabin-Karp pattern search using rolling hash."""
    n, m = len(text), len(pattern)
    matches, comparisons = [], 0

    if m == 0 or m > n:
        return matches, comparisons

    d = 256
    h = pow(d, m - 1, q)
    p_hash = t_hash = 0

    for i in range(m):
        p_hash = (d * p_hash + ord(pattern[i])) % q
        t_hash = (d * t_hash + ord(text[i])) % q

    for s in range(n - m + 1):
        if p_hash == t_hash:
            for k in range(m):
                comparisons += 1
                if text[s + k] != pattern[k]:
                    break
            else:
                matches.append(s)

        if s < n - m:
            t_hash = (d * (t_hash - ord(text[s]) * h) + ord(text[s + m])) % q
            if t_hash < 0:
                t_hash += q

    return matches, comparisons


# --------------------------------------------------------------------------
# Helper / input functions
# --------------------------------------------------------------------------

def get_text_and_pattern():
    """
    Prompts the user to either type their own text/pattern or
    auto-generate random ones. Returns (text, pattern).
    """
    print("\nHow would you like to provide the text and pattern?")
    print("  1. Enter them manually")
    print("  2. Auto-generate random text and pattern")
    choice = input("Choose an option (1/2): ").strip()

    if choice == "1":
        text = input("Enter the text to search in: ").strip()
        pattern = input("Enter the pattern to search for: ").strip()
        if not text or not pattern:
            print("Text and pattern cannot be empty. Please try again.")
            return get_text_and_pattern()
        if len(pattern) > len(text):
            print("Pattern cannot be longer than the text. Please try again.")
            return get_text_and_pattern()
        return text, pattern

    elif choice == "2":
        try:
            text_len = int(input("Length of the text? (e.g. 50): ").strip())
            pattern_len = int(input("Length of the pattern? (e.g. 4): ").strip())
        except ValueError:
            print("Please enter valid integers.")
            return get_text_and_pattern()

        if text_len <= 0 or pattern_len <= 0 or pattern_len > text_len:
            print("Invalid lengths. Pattern must be shorter than or equal to the text.")
            return get_text_and_pattern()

        alphabet = "ABCD"
        text = ''.join(random.choices(alphabet, k=text_len))
        # Grab the pattern from a random spot in the text to guarantee at least one match
        start = random.randint(0, text_len - pattern_len)
        pattern = text[start:start + pattern_len]

        print(f"Generated text:    {text}")
        print(f"Generated pattern: {pattern}")
        return text, pattern

    else:
        print("Invalid choice, please try again.")
        return get_text_and_pattern()


def run_single_search(text, pattern):
    """Runs all three search algorithms once and prints a readable result."""
    display_text = text if len(text) <= 60 else text[:60] + " ..."
    print(f"\nText:    {display_text}")
    print(f"Pattern: {pattern}")

    m1, c1 = naive_search(text, pattern)
    m2, c2 = kmp_search(text, pattern)
    m3, c3 = rabin_karp(text, pattern)

    print("\n--- Results ---")
    print(f"Naive Search  -> Matches at: {m1}, Comparisons: {c1}")
    print(f"KMP           -> Matches at: {m2}, Comparisons: {c2}")
    print(f"Rabin-Karp    -> Matches at: {m3}, Comparisons: {c3}")


def performance_analysis():
    """
    Benchmarks Naive, KMP, and Rabin-Karp across several patterns
    on a large randomly generated text.
    """
    try:
        text_len = input(
            "\nLength of the large text to benchmark on (press Enter for default 10000): "
        ).strip()
        text_len = int(text_len) if text_len else 10000
    except ValueError:
        print("Invalid input, using default length 10000.")
        text_len = 10000

    raw_patterns = input(
        "Enter patterns to test, separated by spaces "
        "(press Enter for default: AB ABCD ABCDAB ABCDABCD): "
    ).strip()
    patterns = raw_patterns.split() if raw_patterns else ["AB", "ABCD", "ABCDAB", "ABCDABCD"]

    text_large = ''.join(random.choices("ABCD", k=text_len))

    print(f"\n{'Pattern':>12} {'Naive':>10} {'KMP':>10} {'RK':>10}")
    print('-' * 50)

    for p in patterns:
        _, c1 = naive_search(text_large, p)
        _, c2 = kmp_search(text_large, p)
        _, c3 = rabin_karp(text_large, p)
        print(f"{p:>12} {c1:>10} {c2:>10} {c3:>10}")


# --------------------------------------------------------------------------
# Main menu
# --------------------------------------------------------------------------

def main():
    print("=" * 60)
    print(" String Matching: Naive vs KMP vs Rabin-Karp - Interactive Demo")
    print("=" * 60)

    while True:
        print("\nMain Menu:")
        print("  1. Search for a pattern in custom/random text")
        print("  2. Run performance benchmark")
        print("  3. Exit")
        choice = input("Choose an option (1/2/3): ").strip()

        if choice == "1":
            text, pattern = get_text_and_pattern()
            run_single_search(text, pattern)

        elif choice == "2":
            performance_analysis()

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
