from flask import Flask, request, jsonify # type: ignore
import os
from flask_cors import CORS
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

app = Flask(__name__)
CORS(app)

@app.route('/api/process', methods=['POST' , 'OPTIONS'])
def process():
    if request.method == 'OPTIONS':
        # Handle OPTIONS request (e.g., return CORS headers)
        response = jsonify({'message': 'CORS preflight request handled'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    

    data = request.json
    input_text = data.get('input')
    
    
    # Call the Jupyter notebook
    output = execute_notebook(input_text)
    return jsonify({'output': output})
def execute_notebook(input_text):
    # Load the notebook
    notebook_path = os.path.join(os.path.dirname(__file__), 'llm.ipynb' )
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)
    
    # Inject the input into the notebook's 4th cell
    nb.cells[3].source = f"input_text = '{input_text}'\n" + nb.cells[3].source
    
    # Execute the notebook
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb, {'metadata': {'path': './'}})
    
    # Extract the output from the last cell
    output = nb.cells[-1].outputs[0]['text']
    return output

if __name__ == '__main__':
    app.run(debug=True)
