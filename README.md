# Compare Match Libs

A Python library that provides 6 different functions to match student names using various string matching libraries. This is particularly useful for matching student names from survey data against ticket registration information.

## Libraries Used

This library implements name matching using the following libraries:
- **Textdistance** - Provides various text distance algorithms
- **Python-Levenshtein** - Fast Levenshtein distance calculation
- **Fuzzywuzzy** - Fuzzy string matching using token-based algorithms
- **Nicknames** - Handles nickname variations and relationships
- **Rapidfuzz** - Fast fuzzy string matching
- **PyNameMatcher** - Specialized name matching with nickname awareness

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Functions

All functions follow the naming convention: `find_best_match_nicknames_<lib_name>`

Each function takes:
- `query_name: str` - The student name from survey
- `possible_names: List[str]` - List of names from ticket registration

Returns:
- `str` - The best matching name from possible_names, or `None` if no good match found

### Available Functions

1. `find_best_match_nicknames_textdistance(query_name, possible_names)`
2. `find_best_match_nicknames_levenshtein(query_name, possible_names)`
3. `find_best_match_nicknames_fuzzywuzzy(query_name, possible_names)`
4. `find_best_match_nicknames_nicknames(query_name, possible_names)`
5. `find_best_match_nicknames_rapidfuzz(query_name, possible_names)`
6. `find_best_match_nicknames_pynamematcher(query_name, possible_names)`

### Convenience Function

`compare_all_matchers(query_name, possible_names)` - Returns a dictionary with results from all matchers.

## Usage Example

```python
from name_matcher import (
    find_best_match_nicknames_textdistance,
    find_best_match_nicknames_nicknames,
    compare_all_matchers
)

# Example usage
query_name = "Bob"
possible_names = ["Robert", "Bobby", "Rob", "Jane", "John"]

# Use a specific matcher
match = find_best_match_nicknames_nicknames(query_name, possible_names)
print(f"Best match: {match}")  # Output: "Robert"

# Compare all matchers
results = compare_all_matchers(query_name, possible_names)
for algorithm, match in results.items():
    print(f"{algorithm}: {match}")
```

## Algorithm Comparison

Different algorithms excel in different scenarios:

- **Nicknames & PyNameMatcher**: Best for handling nickname relationships (Bob -> Robert)
- **TextDistance**: Good general-purpose matching with configurable algorithms
- **FuzzyWuzzy & RapidFuzz**: Excellent for handling misspellings and variations
- **Levenshtein**: Simple edit distance, good for catching typos

## Files

- `name_matcher.py` - Main library with all 6 functions
- `test_name_matcher.py` - Test script to verify functionality
- `example_usage.py` - Example usage demonstrations
- `requirements.txt` - Required dependencies

## Running Tests

```bash
python test_name_matcher.py
```

## Running Examples

```bash
python example_usage.py
```

## Use Case

This library is designed for scenarios where you need to match:
- Student names from survey responses
- Against names from ticket/registration systems
- Where variations, nicknames, and misspellings may occur

The multiple algorithms allow you to choose the best approach for your specific data characteristics.