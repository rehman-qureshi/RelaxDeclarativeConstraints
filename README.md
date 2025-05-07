# Relax Declarative Constraints

This project provides a pipeline for processing PNML files, visualizing Petri net models, creating alpha relations matrices, and finally deriving relaxed declarative constraints.

## Project Structure

- **`driver.py`**: The main entry point of the project. It orchestrates the workflow by calling the visualization, matrix generation, and constraint relaxation functions.
- **`create_alpha_relations_matrix.py`**: Contains the `matrix_function` to generate the alpha relations matrix from a PNML file.
- **`relaxing_declarative_constraints_cmd.py`**: Contains the `relax_constraints_function` to derive relaxed declarative constraints based on the alpha relations matrix.
- **`relaxing_declarative_constraints_gui.py`**: Contains the `main_gui` to populate graphical user interface to derive relaxed declarative constraints based on the alpha relations matrix.
- **`visualize_pnml_model.py`**: Contains the `visualize_function` to visualize the Petri net model from a PNML file.
- **`tutorial.ipynb`**: This notebook provides a brief tutorial on how to use RelaxDeclarativeConstraints tool step-by-step to generate constraints from a business process model.
## Prerequisites

- Python 3.7 or higher
- Required Python libraries (install via `requirements.txt` if available)

## Usage

1. Place your PNML file in the desired location.
2. Run the `driver.py` script with the path to the PNML file as an argument:

   ```bash
   python driver.py <pnml_file_path>