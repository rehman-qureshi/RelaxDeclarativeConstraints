import os
import csv
from find_transitivity import find_transitivity_by_removal
from find_constraints import find_constraints_function
from generate_declare_and_regex import generate_declare_and_regex_function 


# Global variables
directlyFollowSet,eventuallyFollowSet = set(),set()
removedDirectlyFollowSet = set()
affectedEventuallyFollowSet = set()
findTransitivityByRemovalSet = set()

def ask_user_to_remove_constraint(df, last_activities,directlyFollowSet,eventuallyFollowSet):
   
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
                removedDirectlyFollowSet.add(tuple_to_remove)
            else:
                print("Invalid input. No tuple removed.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

        # Update eventuallyFollowSet by removing related constraints
        findTransitivityByRemovalSet.clear()
        transitivity=find_transitivity_by_removal(df,removed_constraints[0], removed_constraints[1], last_activities)
        findTransitivityByRemovalSet.update(transitivity)
        
        for val in findTransitivityByRemovalSet:
            if val in eventuallyFollowSet:
                affectedEventuallyFollowSet.add(val)
                eventuallyFollowSet.remove(val)
        # Show the updated sets
        print("Modified Initial Constraints Set:", len(directlyFollowSet))
        print("Modified Transitive Closed Constraints Set:", len(eventuallyFollowSet))
        for value in eventuallyFollowSet:
            print(value)
        
        print("Affected Transitive Closed Constraints Set:", len(affectedEventuallyFollowSet))
        for value in affectedEventuallyFollowSet:
            print(value)

        user_input = input("Do you want to remove more constraint from the Initial Constraints Set? (yes/no): ").strip().lower()
        if user_input in ['yes']:
            continue
        elif user_input in ['no']:
            break
        else:
            print("Invalid input. Start again to remove constraints.")
            break

    # generate the declarative constraints and regular expressions based on the resulting directly follows relations
    generate_declare_and_regex_function(directlyFollowSet)
    
    # Clear the sets for the next run
    directlyFollowSet.clear()
    eventuallyFollowSet.clear()
    removedDirectlyFollowSet.clear()
    affectedEventuallyFollowSet.clear()



def relax_constraints_function(df, last_activities):
    """
    Main function to derive relaxed declarative constraints.
    """
    directlyFollowSet,eventuallyFollowSet=find_constraints_function(df,last_activities)
  
    ask_user_to_remove_constraint(df, last_activities,directlyFollowSet,eventuallyFollowSet)
    
    return True