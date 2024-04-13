from fuzzywuzzy import fuzz

def fuzzy_search(array, key, query, threshold=70):
    """
    Perform fuzzy search on an array of dictionaries based on a specific key.

    Parameters:
        array (list): List of dictionaries to search through.
        key (str): Key in the dictionaries to perform the search on.
        query (str): Query string to search for.
        threshold (int, optional): Minimum similarity threshold (default is 70).

    Returns:
        list: List of dictionaries that match the fuzzy search.
    """
    results = []
    for item in array:
        if key in item:
            similarity = fuzz.partial_ratio(query.lower(), item[key].lower())
            if similarity >= threshold:
                results.append(item)
    return results
