"""
Example usage of the name matching library.

This script demonstrates how to use the different name matching functions
to find the best match for student names from survey data against
ticket registration information.
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


def main():
    """Demonstrate usage of the name matching functions."""
    
    print("Student Name Matching Demo")
    print("=" * 50)
    
    # Example 1: First names only (easier matching)
    print("Example 1: First names only")
    print("-" * 30)
    survey_names = ["Bob", "Mike", "Liz", "Bill"]
    ticket_names = ["Robert", "Michael", "Elizabeth", "William", "Jane", "David"]
    
    print(f"Survey names: {survey_names}")
    print(f"Ticket names: {ticket_names}")
    print()
    
    for survey_name in survey_names:
        print(f"Matches for '{survey_name}':")
        results = compare_all_matchers(survey_name, ticket_names)
        for algorithm, match in results.items():
            print(f"  {algorithm:15}: {match}")
        print()
    
    # Example 2: Full names (more realistic scenario)
    print("Example 2: Full names from registration")
    print("-" * 40)
    survey_names = ["Bob", "Mike", "Liz", "Bill", "Johnny"]
    ticket_names = ["Robert Smith", "Michael Johnson", "Elizabeth Brown", 
                   "William Davis", "Jonathan Wilson", "Jane Doe", "David Lee"]
    
    print(f"Survey names: {survey_names}")
    print(f"Ticket names: {ticket_names}")
    print()
    
    for survey_name in survey_names:
        print(f"Matches for '{survey_name}':")
        results = compare_all_matchers(survey_name, ticket_names)
        matches_found = any(match is not None for match in results.values())
        if matches_found:
            for algorithm, match in results.items():
                if match:
                    print(f"  {algorithm:15}: {match}")
        else:
            print("  No matches found with any algorithm")
        print()
    
    # Example 3: Demonstrate individual function usage
    print("Example 3: Individual function usage")
    print("-" * 35)
    query = "Johnny"
    names = ["Jonathan", "John", "Jon", "Johnny", "Jane"]
    
    print(f"Query: '{query}'")
    print(f"Possible names: {names}")
    print()
    
    # Show usage of individual functions
    from name_matcher import find_best_match_nicknames_nicknames
    
    match = find_best_match_nicknames_nicknames(query, names)
    print(f"Best match using nicknames library: {match}")
    
    # Show how you might use this in practice
    print()
    print("Practical usage example:")
    print("if match:")
    print("    print(f'Student {query} matches registration {match}')")
    print("else:")
    print("    print(f'No match found for {query}')")
    
    if match:
        print(f"Student {query} matches registration {match}")
    else:
        print(f"No match found for {query}")


if __name__ == "__main__":
    main()