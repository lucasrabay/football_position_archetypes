import bs4

class Utils:
    
    def __init__(self):
        pass
    
    @staticmethod
    def subdivide_list(lst, n):
        """
        Splits a list into sublists of a specified size.

        Parameters:
        lst (list): The list to be subdivided.
        n (int): The number of elements each sublist should contain.

        Returns:
        list: A list of sublists, each with a maximum of n elements.

        Raises:
        ValueError: If `lst` is not a list or `n` is not a positive integer.
        """
        if not isinstance(lst, list):
            raise ValueError("The first parameter must be a list.")
        if not isinstance(n, int) or n <= 0:
            raise ValueError("The second parameter must be a positive integer.")

        # Create and return the subdivided list
        return [lst[i:i + n] for i in range(0, len(lst), n)]
    
    @staticmethod
    def extract_raw_data(data, tag):
        """
        Extracts the raw data from the data object.

        Parameters:
        data (any): The data object to extract the raw data from.
        tag (str): The tag to search for in the data object.

        Returns:
        any: The raw data extracted from the data object.
        
        Raises:
        ValueError: If the data is not a 'bs4.element.ResultSet' object or if the required tag is not found.
        """
        if not isinstance(data, (bs4.element.ResultSet, list)):
            raise ValueError("The first parameter must be a supported object.")
        
        # Filter data by the specified tag and check if any matches are found
        filtered_data = [item for item in data if item.name == tag]
        if not filtered_data:
            raise ValueError(f"No '{tag}' tags found in the provided 'ResultSet' data.")
        
        # Extract text from each matching element
        column_data = [item.text for item in filtered_data]
        return column_data
        