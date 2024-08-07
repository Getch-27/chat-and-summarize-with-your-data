from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from llm import load_document_and_split, embed_documents, setup_retrieval_chain, handle_chat

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

context = None
vectordb = None
qa = None

@app.route('/api/load_document', methods=['POST'])
def load_document():
    global context, qa ,vectordb

    if 'document' not in request.files:
        return jsonify({'error': 'Document not provided'}), 400

    file = request.files['document']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        document_path = os.path.join('./uploads', file.filename)
        file.save(document_path)

        context = load_document_and_split(document_path)
        vectordb = embed_documents(context)
        # qa = setup_retrieval_chain(vectordb)

        return jsonify({'message': 'Document loaded and embedded successfully'})

@app.route('/api/chat', methods=['POST'])
def chat():
    global qa
    global vectordb
    qa =setup_retrieval_chain(vectordb)

    if qa is None:
        return jsonify({'error': 'No document loaded. Please load a document first.'}), 400

    data = request.json
    question = data.get('question')

    if not question:
        return jsonify({'error': 'Question not provided'}), 400

    answer = handle_chat(qa, question)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
