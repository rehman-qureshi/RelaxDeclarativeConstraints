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
    visualize_function(pnml_path)
   
    # Call the matrix function
    df, last_transitions  = matrix_function(pnml_path)
    if df is not None:
        print("Return Alpha Relations Matrix in driver.py file.")
        # Fetch the last transition label or name
        # If the label is not available, use the name
        last_transition = next(iter(last_transitions)).label if next(iter(last_transitions)).label else next(iter(last_transitions)).name
        # Call the relax constraints function
        relax_constraints_function(df,last_transition,pnml_path)
        
    else:
        print("Failed to create the alpha relations matrix.")
 
   