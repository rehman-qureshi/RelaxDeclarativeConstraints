

# Global variables
directlyFollowSet = set()
eventuallyFollowSet = set()

def find_eventually_follow(df, columns_names, previous_value, search_value, last_activities):
    """
    Iteratively find all eventually follow constraints using a stack with cycle detection.
    """
    global eventuallyFollowSet

    # Use a stack to replace recursion
    stack = [(previous_value, search_value)]
    visited = set()  # Track visited nodes to avoid cycles

    while stack:
        prev, current = stack.pop()

        # Skip if already visited to avoid cycles
        if current in visited:
            continue
        visited.add(current)

        # Base case: Stop if current matches last_activities
        if current in last_activities:
            continue

        # Filter rows where the first column matches the current value
        filtered_rows = df.loc[df.iloc[:, 0] == current]
        if filtered_rows.empty:
            continue

        # Iterate through the filtered rows
        for _, row in filtered_rows.iterrows():
            for col_index, col_value in enumerate(row):
                if isinstance(col_value, str) and '→' in col_value:
                    #if columns_names[col_index] == last_transition:
                    if columns_names[col_index] in last_activities:
                        eventuallyFollowSet.add((prev, columns_names[col_index]))
                    else:
                        eventuallyFollowSet.add((prev, columns_names[col_index]))
                        stack.append((prev, columns_names[col_index]))
                        #print(f"Added to stack: prev={prev}, next={columns_names[col_index]}")

def initialize_directly_follow_set(df, columns_names):
    """
    Initialize the directlyFollowSet by iterating through the DataFrame.
    """
    global directlyFollowSet

    # Use vectorized operations to populate directlyFollowSet
    for row_index in range(len(df)):
        for col_index in range(1, len(df.columns)):
            cell_value = df.iloc[row_index, col_index]
            if isinstance(cell_value, str) and ('→' in cell_value or '||' in cell_value):
                directlyFollowSet.add((df.iloc[row_index, 0], columns_names[col_index]))

    print("Initial Constraints Set is determining ... ")


def process_constraints(df, columns_names, last_activities):
    global eventuallyFollowSet, directlyFollowSet

    # Find all eventually follow constraints
    for idx, value in enumerate(directlyFollowSet):
        #print(f"Processing directlyFollowSet item {idx + 1}/{len(directlyFollowSet)}: {value}")
        find_eventually_follow(df, columns_names, value[0], value[1], last_activities)

    print("Length of Initial Constraints Set:", len(directlyFollowSet))

    # Remove duplicates from eventuallyFollowSet
    eventuallyFollowSet -= directlyFollowSet


def find_constraints_function(df, last_activities):
    """
    Main function to find all possible constraints.
    """
    global directlyFollowSet, eventuallyFollowSet

    directlyFollowSet.clear()
    eventuallyFollowSet.clear()
    # Get column names
    columns_names = df.columns.tolist()

    # Initialize directlyFollowSet
    initialize_directly_follow_set(df, columns_names)
    
    # Process constraints
    # You can change this to any other transition as needed
    process_constraints(df, columns_names, last_activities)

    return directlyFollowSet, eventuallyFollowSet
    
    
    