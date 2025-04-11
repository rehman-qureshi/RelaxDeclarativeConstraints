# Alpha Relations Matrix Project

This project is designed to generate an alpha relations matrix from a Petri net model provided in PNML format. The alpha relations matrix is useful for analyzing the behavior of the Petri net and understanding the relationships between transitions.

## Project Structure

```
alpha-relations-matrix-project
├── data
│   └── model_d.pnml          # Petri net model in PNML format
├── notebooks
│   └── generate_alpha_relations_matrix.ipynb  # Jupyter Notebook for generating the matrix
├── src
│   ├── create_alpha_relations_matrix.py        # Main logic for creating the alpha relations matrix
│   └── utils
│       └── __init__.py                          # Initialization file for the utils module
├── requirements.txt                             # List of dependencies
└── README.md                                    # Project documentation
```

## Requirements

To run this project, you need to install the following dependencies:

- pandas
- openpyxl

You can install the required packages using pip:

```
pip install -r requirements.txt
```

## Usage

1. Place your PNML file in the `data` directory. The provided example is `model_d.pnml`.
2. Open the Jupyter Notebook `notebooks/generate_alpha_relations_matrix.ipynb`.
3. Run the cells in the notebook to generate the alpha relations matrix.

## License

This project is licensed under the MIT License.