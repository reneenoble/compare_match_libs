"""
Test script for the name matching functions.
"""

from name_matcher import (
    find_best_match_nicknames_textdistance,
    find_best_match_nicknames_levenshtein, 
    find_best_match_nicknames_fuzzywuzzy,
    find_best_match_nicknames_nicknames,
    find_best_match_nicknames_rapidfuzz,
    find_best_match_nicknames_pynamematcher,
    compare_all_matchers
)


def test_basic_functionality():
    """Test that all functions work with basic input."""
    query_name = "John"
    possible_names = ["Jonathan", "Jon", "Johnny", "Jane", "Bob"]
    
    print("Testing basic functionality:")
    print(f"Query: {query_name}")
    print(f"Possible names: {possible_names}")
    print()
    
    # Test each function
    functions = [
        ("textdistance", find_best_match_nicknames_textdistance),
        ("levenshtein", find_best_match_nicknames_levenshtein),
        ("fuzzywuzzy", find_best_match_nicknames_fuzzywuzzy),
        ("nicknames", find_best_match_nicknames_nicknames),
        ("rapidfuzz", find_best_match_nicknames_rapidfuzz),
        ("pynamematcher", find_best_match_nicknames_pynamematcher),
    ]
    
    for name, func in functions:
        try:
            result = func(query_name, possible_names)
            print(f"{name:15}: {result}")
        except Exception as e:
            print(f"{name:15}: ERROR - {e}")
    
    print("\nCompare all matchers:")
    results = compare_all_matchers(query_name, possible_names)
    for matcher, result in results.items():
        print(f"{matcher:15}: {result}")


def test_edge_cases():
    """Test edge cases."""
    print("\n" + "="*50)
    print("Testing edge cases:")
    
    # Empty inputs
    print("\nEmpty query name:")
    result = find_best_match_nicknames_textdistance("", ["John", "Jane"])
    print(f"Result: {result}")
    
    print("\nEmpty possible names:")
    result = find_best_match_nicknames_textdistance("John", [])
    print(f"Result: {result}")
    
    # No good matches
    print("\nNo good matches:")
    result = find_best_match_nicknames_textdistance("Xyzzyx", ["John", "Jane", "Bob"])
    print(f"Result: {result}")
    
    # Case sensitivity
    print("\nCase sensitivity test:")
    query = "JOHN"
    names = ["john", "John", "JOHN"]
    result = find_best_match_nicknames_textdistance(query, names)
    print(f"Query: {query}, Names: {names}, Result: {result}")


def test_nickname_variations():
    """Test nickname handling."""
    print("\n" + "="*50)
    print("Testing nickname variations:")
    
    test_cases = [
        ("Bob", ["Robert", "Bobby", "Rob"]),
        ("Bill", ["William", "Billy", "Will"]),
        ("Mike", ["Michael", "Mickey", "Mick"]),
        ("Liz", ["Elizabeth", "Lizzy", "Beth"]),
    ]
    
    for query, names in test_cases:
        print(f"\nQuery: {query}, Possible: {names}")
        results = compare_all_matchers(query, names)
        for matcher, result in results.items():
            print(f"  {matcher:15}: {result}")


if __name__ == "__main__":
    test_basic_functionality()
    test_edge_cases()
    test_nickname_variations()
    print("\nAll tests completed!")