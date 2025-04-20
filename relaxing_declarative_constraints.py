import pandas as pd
import sys
from collections import deque
import os
import csv


# Global variables
directlyFollowSet = set()
eventuallyFollowSet = set()

def find_eventually_follow(df, columns_names, previous_value, search_value, last_transition):
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

        # Base case: Stop if current matches last_transition
        #if current == last_transition:
        if current in last_transition:
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
                    if columns_names[col_index] in last_transition:
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

    print("Initial Constraints Set is determining ... : ", len(directlyFollowSet))


def process_constraints(df, columns_names, last_transition):
    global eventuallyFollowSet, directlyFollowSet

    # Find all eventually follow constraints
    for idx, value in enumerate(directlyFollowSet):
        #print(f"Processing directlyFollowSet item {idx + 1}/{len(directlyFollowSet)}: {value}")
        find_eventually_follow(df, columns_names, value[0], value[1], last_transition)

    print("Length of Initial Constraints Set:", len(directlyFollowSet))

    # Remove duplicates from eventuallyFollowSet
    eventuallyFollowSet -= directlyFollowSet
    print("Length of Transitive Closed Constraints Set:", len(eventuallyFollowSet))
    print("Current Set of Transitive Closed Constraints:")
    # Print the eventuallyFollowSet
    for value in eventuallyFollowSet:
        print(value)
    
    # Combine both sets
    #combinedSet = eventuallyFollowSet.union(directlyFollowSet)
    #print("Length of Combined Set:", len(combinedSet))


def ask_user_to_remove_constraint(pnml_path):
    """
    Allow the user to remove a constraint from directlyFollowSet and update eventuallyFollowSet.
    """
    global directlyFollowSet, eventuallyFollowSet

    while True:

        if len(directlyFollowSet) == 0:  # if no constraints left to remove
            print("No more constraints to remove. Exiting...")
            break

    # Show all tuples in directlyFollowSet
        print("Current Set of Initial Constraints:")
        directlyFollowList = list(directlyFollowSet)  # Convert to list once for indexing
        for idx, value in enumerate(directlyFollowList):
            print(f"{idx + 1}: {value}")

        removed_constraints = []
        # Ask the user which constraint to be removed
        try:
            user_input = int(input("Enter the number of the constraint you want to remove (e.g., 1, 2, etc.): "))
            if 1 <= user_input <= len(directlyFollowList):
                tuple_to_remove = directlyFollowList[user_input - 1]
                directlyFollowSet.remove(tuple_to_remove)
                print(f"Removed Constraint: {tuple_to_remove}")
                removed_constraints.extend(tuple_to_remove)
            else:
                print("Invalid input. No tuple removed.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

        # Update eventuallyFollowSet by removing related constraints
        to_remove = [value for value in eventuallyFollowSet if value[0] in removed_constraints or value[1] in removed_constraints]
        for value in to_remove:
            eventuallyFollowSet.remove(value)

        # Show the updated sets
        print("Updated Initial Constraints Set:", len(directlyFollowSet))
        print("Updated Transitive Closed Constraints Set:", len(eventuallyFollowSet))
        for value in eventuallyFollowSet:
            print(value)
        
        user_input = input("Do you want to remove more constraint from the Initial Constraints Set? (yes/no): ").strip().lower()
        if user_input in ['yes']:
            continue
        elif user_input in ['no']:
            break
        else:
            print("Invalid input. Start again to remove constraints.")
            break

    # Save the updated sets to CSV files
    # Define the output folder path relative to the driver.py location
    driver_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
    output_dir = os.path.join(driver_dir, "output")
    os.makedirs(output_dir, exist_ok=True)  # Create the folder if it doesn't exist
        # Define the output file path
    output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(pnml_path))[0]+"_declarative_constraints.csv")


    # Write to a single-column CSV file
    with open(output_file, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)

        # First column section: "Initial Constraints Set"
        writer.writerow(["**Initial Constraints Set**"])
        for tup in directlyFollowSet:
            writer.writerow([str(tup)])  # Write full tuple as a string


        # Second column section: "Transitive Closed Constraints Set"
        writer.writerow(["**Transitive Closed Constraints Set**"])
        for tup in eventuallyFollowSet:
            writer.writerow([str(tup)])
    
    # Get the relative path of the output file
    relative_output_file = os.path.relpath(output_file, start=os.getcwd())
    print(f"Updated constraints saved to {relative_output_file}")
    # Clear the sets for the next run
    directlyFollowSet.clear()
    eventuallyFollowSet.clear()

def find_all_possible_constraints(df, last_transitions):
    """
    Main function to find all possible constraints.
    """
    global directlyFollowSet, eventuallyFollowSet

    # Get column names
    columns_names = df.columns.tolist()

    # Initialize directlyFollowSet
    initialize_directly_follow_set(df, columns_names)
    
    # Process constraints
    # You can change this to any other transition as needed
    process_constraints(df, columns_names, last_transitions)


def relax_constraints_function(df, last_transitions, pnml_path):
    """
    Main function to derive relaxed declarative constraints.
    """

    find_all_possible_constraints(df, last_transitions)
    ask_user_to_remove_constraint(pnml_path)
    
    return True