import os
import nbformat

def clean_notebook_output(notebook_path):
    """Clears the output of a Jupyter notebook."""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)
    
    # Clear outputs for each cell
    for cell in notebook.cells:
        if cell.cell_type == 'code':
            cell.outputs = []
            cell.execution_count = None
    
    # Save the cleaned notebook
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbformat.write(notebook, f)

def clean_notebooks_in_folder(folder_path):
    """Cleans all Jupyter notebooks in the specified folder."""
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return
    
    notebook_count = 0
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.ipynb') and not file.startswith('.'):  # Skip hidden files
                notebook_path = os.path.join(root, file)
                print(f"Cleaning: {notebook_path}")
                clean_notebook_output(notebook_path)
                notebook_count += 1
    
    print(f"Successfully cleaned {notebook_count} Jupyter notebooks.")

if __name__ == "__main__":
    src_folder = "src"
    clean_notebooks_in_folder(src_folder)