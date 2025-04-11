import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import os


# Global variables
finalRelaxedConstraints = []
finalRemovedConstraints = []

def find_constraints(df, columns_names, search_value, last_transition, visited):
    """
    Function to find constraints based on search_value and last_transition.
    """
    stack = [(search_value, [])]  # Stack to simulate recursion (search_value and removedHelper)
    localRelaxedConstraints = []
    localRemovedConstraints = []

    while stack:
        current_value, current_helper = stack.pop()

        # Skip if already visited to avoid cycles
        if current_value in visited:
            continue
        visited.add(current_value)

        # Base case: Stop if current_value matches last_transition
        if current_value == last_transition:
            if current_value not in localRelaxedConstraints:
                localRelaxedConstraints.append(current_value)
            continue

        # Filter rows where the first column matches the current_value
        filtered_row = df[df.iloc[:, 0] == current_value]
        if filtered_row.empty:
            continue

        # Iterate through the filtered rows
        for _, row in filtered_row.iterrows():
            for col_index, col_value in enumerate(row):
                if isinstance(col_value, str) and '→' in col_value:
                    if columns_names[col_index] == last_transition:
                        if columns_names[col_index] not in localRelaxedConstraints:
                            localRelaxedConstraints.append(columns_names[col_index])
                        removedHelperAll = "".join(current_helper)
                        localRemovedConstraints.append(removedHelperAll + current_value + ' → ' + columns_names[col_index])
                        continue
                    else:
                        # Add the next value to the stack
                        stack.append((columns_names[col_index], current_helper + [current_value + ' → ']))

    return localRelaxedConstraints, localRemovedConstraints

def process_constraints_for_key(df, columns_names, key, value, last_transition):
    """
    Process constraints for a single key-value pair in the result dictionary.
    """
    localRelaxedConstraints = []
    localRemovedConstraints = []

    visited = set()  # Track visited nodes to avoid cycles

    for eachValue in value:
        relaxed, removed = find_constraints(df, columns_names, eachValue, last_transition, visited)

        # Add relaxed constraints
        for eachRelaxed in relaxed:
            localRelaxedConstraints.append(key + ' → ' + eachRelaxed)

        # Add removed constraints
        if removed:
            localRemovedConstraints.append(key + ' → ' + eachValue)
            for eachRemoved in removed:
                if eachRemoved != eachValue:
                    localRemovedConstraints.append(key + ' → ' + eachRemoved)

    return localRelaxedConstraints, localRemovedConstraints

def process_constraints(df, result, columns_names, last_transition):
    """
    Process constraints for each key-value pair in the result dictionary using threading.
    """
    global finalRelaxedConstraints, finalRemovedConstraints

    with ThreadPoolExecutor() as executor:
        futures = []
        for key, value in result.items():
            #print(f"Processing key: {key} with values: {value}")
            futures.append(executor.submit(process_constraints_for_key, df, columns_names, key, value, last_transition))

        for future in futures:
            localRelaxedConstraints, localRemovedConstraints = future.result()
            finalRelaxedConstraints.extend(localRelaxedConstraints)
            finalRemovedConstraints.extend(localRemovedConstraints)

    # Remove duplicates from final results
    finalRelaxedConstraints[:] = list(set(finalRelaxedConstraints))
    finalRemovedConstraints[:] = list(set(finalRemovedConstraints))

def relax_constraints_function(df, last_transition,pnml_path):
    """
    Main function to read the data, process constraints, and print results.
    """
    global finalRelaxedConstraints, finalRemovedConstraints


    # Initialize a dictionary to store row indices and corresponding column names
    result = {}

    # Get column names
    columns_names = df.columns.tolist()

    # Build the result dictionary
    for row_index in range(len(df)):
        list_of_columns = []
        for col_index in range(1, len(df.columns)):
            cell_value = df.iloc[row_index, col_index]
            if isinstance(cell_value, str) and ('→' in cell_value or '||' in cell_value):
                list_of_columns.append(columns_names[col_index])
        result[df.iloc[row_index, 0]] = list_of_columns

    # Process constraints
    process_constraints(df, result, columns_names, last_transition)

    # Save results to an Excel file
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)  # Create the folder if it doesn't exist
    output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(pnml_path))[0]+"_relaxed_removed_constraints.xlsx")

    # Ensure both lists have the same length
    max_length = max(len(finalRelaxedConstraints), len(finalRemovedConstraints))
    finalRelaxedConstraints.extend([""] * (max_length - len(finalRelaxedConstraints)))
    finalRemovedConstraints.extend([""] * (max_length - len(finalRemovedConstraints)))

    # Create a DataFrame with two columns
    constraints_df = pd.DataFrame({
        "Relaxed Constraints": finalRelaxedConstraints,
        "Removed Constraints": finalRemovedConstraints
    })

    # Save the DataFrame to an Excel file
    constraints_df.to_excel(output_file, index=False, engine="openpyxl")
    print(f"Constraints saved to {output_file}")

