import sys
from create_alpha_relations_matrix import matrix_function
from relaxing_declarative_constraints import relax_constraints_function
from visualize_pnml_model import visualize_function

if __name__ == "__main__":
     
    if len(sys.argv) != 2:
        print("Usage: python driver.py <pnml_file_path>")
        sys.exit(1)

    pnml_path = sys.argv[1]
    # Call the visualization function
    output_file=visualize_function(pnml_path)
   
    # Call the matrix function
    df, last_transitions  = matrix_function(pnml_path)
    if df is not None:
        print("Return Alpha Relations Matrix in driver.py file.")
        # Fetch the last transitions
        print("Last transitions: ", last_transitions)                   
        # Call the relax constraints function
        constraints_df=relax_constraints_function(df,last_transitions,pnml_path)
        if constraints_df is not True:
            print("Failed to derived relaxed declarative constraints.")
        
    else:
        print("Failed to create the alpha relations matrix.")
 
   