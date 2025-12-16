# Function to display a string if the input is of type string
# Returns the string if successful, otherwise returns None
# Handles exceptions gracefully

def display_string(value):
    try:
        if isinstance(value, str):
            print(value)
            return value
        else:
            return None
    except Exception as e:
        return None

# Example usage
if __name__ == "__main__":
    # Test with string
    result1 = display_string("Hello World")
    print("Returned:", result1)
    
    # Test with non-string
    result2 = display_string(123)
    print("Returned:", result2)

    # note: The function will return None for non-string inputs without raising an exception
    # Test with None
    result3 = display_string(None)
    print("Returned:", result3)
    # Test with list
    result4 = display_string([1, 2, 3])
    print("Returned:", result4)
    # Test with dictionary
    result5 = display_string({"key": "value"})
    print("Returned:", result5)



    
