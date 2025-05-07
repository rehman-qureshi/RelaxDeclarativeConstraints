

findTransitivityByRemovalSet = set()

def find_transitivity_function(df, columns_names, previous_value, search_value, last_activities):
    """
    Iteratively find all eventually follow constraints using a stack with cycle detection.
    """
    global findTransitivityByRemovalSet
    # Use a stack to replace recursion
    stack = [(previous_value, search_value)]
    visited = set()  # Track visited nodes to avoid cycles

    while stack:
        prev, current = stack.pop()

        # Skip if already visited to avoid cycles
        if current in visited:
            continue
        visited.add(current)

        # Base case: Stop if current matches last_transition
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
                    if columns_names[col_index] in last_activities:
                        findTransitivityByRemovalSet.add((prev, columns_names[col_index]))
                    else:
                        findTransitivityByRemovalSet.add((prev, columns_names[col_index]))
                        stack.append((prev, columns_names[col_index]))
                        #print(f"Added to stack: prev={prev}, next={columns_names[col_index]}")


def find_transitivity_by_removal(df, previous_value, search_value, last_activities):
    columns_names = df.columns.tolist()
    findTransitivityByRemovalSet.clear()
    find_transitivity_function(df, columns_names, previous_value, search_value, last_activities)

    return findTransitivityByRemovalSet