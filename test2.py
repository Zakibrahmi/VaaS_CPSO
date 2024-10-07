# Given set of tuples
tuples = [(1, 2), (2, 3), (3, 4), (4, 5), (1, 5), (5, 6), 
          (6, 7), (7, 8), (8, 6), (8, 9), (9, 10), (10, 11), 
          (11, 12), (12, 13)]

# Array of items to check for in the first position
array = [1, 2, 3, 4,  5]

# Find tuples where the first item is in the array and the second item is not
filtered_tuples = [t for t in tuples if t[0] in array and t[1] not in array]

# Define a list of tuples
array_of_tuples = [(1, 2), (3, 4), (5, 6), (7, 8)]

# Define the tuple to check
item1, item2 = 3, 4
tuple_to_check = (item1, item2)
reversed_tuple = (item2, item1)

# Check if either the tuple or its reversed form exists in the list
if tuple_to_check in array_of_tuples or reversed_tuple in array_of_tuples:
    print(f"One of the tuples {tuple_to_check} or {reversed_tuple} exists in the list.")
else:
    print(f"Neither the tuple {tuple_to_check} nor {reversed_tuple} exists in the list.")