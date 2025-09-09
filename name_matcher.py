"""
Student Name Matching Library

This module provides functions to match student names using various string matching libraries.
Each function follows the naming convention: find_best_match_nicknames_<lib_name>

Each function takes:
- query_name: str - The student name from survey
- possible_names: list[str] - List of names from ticket registration

Returns:
- str - The best matching name from possible_names, or None if no good match found
"""

import textdistance
import Levenshtein
import fuzzywuzzy.fuzz
import nicknames
import rapidfuzz.fuzz
import pynamematcher
from typing import List, Optional


def find_best_match_nicknames_textdistance(query_name: str, possible_names: List[str]) -> Optional[str]:
    """
    Find the best match using the textdistance library with Jaro-Winkler similarity.
    
    Args:
        query_name: The name to search for
        possible_names: List of candidate names
        
    Returns:
        The best matching name or None if no good match found
    """
    if not query_name or not possible_names:
        return None
        
    query_name = query_name.strip().lower()
    best_match = None
    best_score = 0.0
    
    for name in possible_names:
        if not name:
            continue
        name_clean = name.strip().lower()
        # Using Jaro-Winkler which is good for names
        score = textdistance.jaro_winkler(query_name, name_clean)
        if score > best_score:
            best_score = score
            best_match = name
    
    # Return match only if score is above threshold
    return best_match if best_score > 0.6 else None


def find_best_match_nicknames_levenshtein(query_name: str, possible_names: List[str]) -> Optional[str]:
    """
    Find the best match using the Python-Levenshtein library.
    
    Args:
        query_name: The name to search for
        possible_names: List of candidate names
        
    Returns:
        The best matching name or None if no good match found
    """
    if not query_name or not possible_names:
        return None
        
    query_name = query_name.strip().lower()
    best_match = None
    best_distance = float('inf')
    
    for name in possible_names:
        if not name:
            continue
        name_clean = name.strip().lower()
        distance = Levenshtein.distance(query_name, name_clean)
        if distance < best_distance:
            best_distance = distance
            best_match = name
    
    # Return match only if distance is reasonable (less than half the query name length)
    max_distance = len(query_name) // 2 + 1
    return best_match if best_distance <= max_distance else None


def find_best_match_nicknames_fuzzywuzzy(query_name: str, possible_names: List[str]) -> Optional[str]:
    """
    Find the best match using the fuzzywuzzy library.
    
    Args:
        query_name: The name to search for
        possible_names: List of candidate names
        
    Returns:
        The best matching name or None if no good match found
    """
    if not query_name or not possible_names:
        return None
        
    query_name = query_name.strip()
    best_match = None
    best_score = 0
    
    for name in possible_names:
        if not name:
            continue
        name_clean = name.strip()
        # Using token_sort_ratio which handles different name orders well
        score = fuzzywuzzy.fuzz.token_sort_ratio(query_name, name_clean)
        if score > best_score:
            best_score = score
            best_match = name
    
    # Return match only if score is above threshold
    return best_match if best_score > 60 else None


def find_best_match_nicknames_nicknames(query_name: str, possible_names: List[str]) -> Optional[str]:
    """
    Find the best match using the nicknames library to handle nickname variations.
    
    Args:
        query_name: The name to search for
        possible_names: List of candidate names
        
    Returns:
        The best matching name or None if no good match found
    """
    if not query_name or not possible_names:
        return None
        
    query_name = query_name.strip().lower()
    nn = nicknames.NickNamer()
    
    # Get all possible nicknames for the query name
    query_nicknames = nn.nicknames_of(query_name)
    query_nicknames.add(query_name)  # Include the original name
    
    best_match = None
    best_score = 0
    
    for name in possible_names:
        if not name:
            continue
        name_clean = name.strip().lower()
        
        # Check if name matches any nickname of query
        if name_clean in query_nicknames:
            return name  # Exact nickname match
        
        # Check if query matches any nickname of this candidate name
        name_nicknames = nn.nicknames_of(name_clean)
        name_nicknames.add(name_clean)
        
        if query_name in name_nicknames:
            return name  # Query is a nickname of this candidate
        
        # Check for intersection of nickname sets
        intersection = query_nicknames.intersection(name_nicknames)
        if intersection:
            return name  # Common nicknames found
        
        # Fallback to fuzzy matching
        score = fuzzywuzzy.fuzz.ratio(query_name, name_clean)
        if score > best_score:
            best_score = score
            best_match = name
    
    # Return match only if score is above threshold
    return best_match if best_score > 70 else None


def find_best_match_nicknames_rapidfuzz(query_name: str, possible_names: List[str]) -> Optional[str]:
    """
    Find the best match using the rapidfuzz library.
    
    Args:
        query_name: The name to search for
        possible_names: List of candidate names
        
    Returns:
        The best matching name or None if no good match found
    """
    if not query_name or not possible_names:
        return None
        
    query_name = query_name.strip()
    best_match = None
    best_score = 0.0
    
    for name in possible_names:
        if not name:
            continue
        name_clean = name.strip()
        # Using token_sort_ratio which handles different name orders well
        score = rapidfuzz.fuzz.token_sort_ratio(query_name, name_clean)
        if score > best_score:
            best_score = score
            best_match = name
    
    # Return match only if score is above threshold
    return best_match if best_score > 60.0 else None


def find_best_match_nicknames_pynamematcher(query_name: str, possible_names: List[str]) -> Optional[str]:
    """
    Find the best match using the PyNameMatcher library.
    
    Args:
        query_name: The name to search for
        possible_names: List of candidate names
        
    Returns:
        The best matching name or None if no good match found
    """
    if not query_name or not possible_names:
        return None
        
    matcher = pynamematcher.PyNameMatcher()
    query_name = query_name.strip().lower()
    
    # Get all possible matches for the query name
    try:
        query_matches = matcher.match(query_name, query_name)
        query_matches.add(query_name)  # Include the original name
    except Exception:
        query_matches = {query_name}
    
    # Check each possible name
    for name in possible_names:
        if not name:
            continue
        name_clean = name.strip().lower()
        
        # Direct match
        if name_clean == query_name:
            return name
        
        # Check if the candidate name is in query matches
        if name_clean in query_matches:
            return name
            
        # Check if query name is in candidate matches
        try:
            name_matches = matcher.match(name_clean, name_clean)
            if query_name in name_matches:
                return name
        except Exception:
            continue
    
    # Fallback to fuzzy matching if no direct matches
    best_match = None
    best_score = 0
    
    for name in possible_names:
        if not name:
            continue
        name_clean = name.strip()
        score = fuzzywuzzy.fuzz.ratio(query_name, name_clean.lower())
        if score > best_score:
            best_score = score
            best_match = name
    
    # Return match only if score is above threshold
    return best_match if best_score > 70 else None


# Convenience function to test all matchers
def compare_all_matchers(query_name: str, possible_names: List[str]) -> dict:
    """
    Compare results from all matching functions.
    
    Args:
        query_name: The name to search for
        possible_names: List of candidate names
        
    Returns:
        Dictionary with results from each matcher
    """
    return {
        'textdistance': find_best_match_nicknames_textdistance(query_name, possible_names),
        'levenshtein': find_best_match_nicknames_levenshtein(query_name, possible_names),
        'fuzzywuzzy': find_best_match_nicknames_fuzzywuzzy(query_name, possible_names),
        'nicknames': find_best_match_nicknames_nicknames(query_name, possible_names),
        'rapidfuzz': find_best_match_nicknames_rapidfuzz(query_name, possible_names),
        'pynamematcher': find_best_match_nicknames_pynamematcher(query_name, possible_names),
    }