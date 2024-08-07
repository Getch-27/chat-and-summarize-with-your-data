import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [document, setDocument] = useState(null);
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);

  const handleDocumentChange = (e) => {
    setDocument(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!document) {
      alert('Please select a document to upload');
      return;
    }

    const formData = new FormData();
    formData.append('document', document);

    try {
      setLoading(true);
      const response = await axios.post('http://127.0.0.1:5000/api/load_document', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      alert(response.data.message);
    } catch (error) {
      console.error('Error uploading document:', error);
      alert('Error uploading document');
    } finally {
      setLoading(false);
    }
  };

  const handleQuestionChange = (e) => {
    setQuestion(e.target.value);
  };

  const handleChat = async () => {
    if (!question) {
      alert('Please enter a question');
      return;
    }

    try {
      setLoading(true);
      const response = await axios.post('http://127.0.0.1:5000/api/chat', { question });
      setAnswer(response.data.answer);
    } catch (error) {
      console.error('Error getting answer:', error);
      alert('Error getting answer');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Document Upload and Chat</h1>

      <div className="mb-4">
        <input type="file" onChange={handleDocumentChange} className="mb-2" />
        <button
          onClick={handleUpload}
          disabled={loading}
          className="bg-blue-500 text-white px-4 py-2 rounded"
        >
          {loading ? 'Uploading...' : 'Upload Document'}
        </button>
      </div>

      <div className="mb-4">
        <textarea
          value={question}
          onChange={handleQuestionChange}
          placeholder="Enter your question"
          className="w-full p-2 border rounded mb-2"
        />
        <button
          onClick={handleChat}
          disabled={loading}
          className="bg-green-500 text-white px-4 py-2 rounded"
        >
          {loading ? 'Processing...' : 'Ask Question'}
        </button>
      </div>

      {answer && (
        <div className="mt-4 p-4 border rounded bg-gray-100">
          <h2 className="text-xl font-bold">Answer:</h2>
          <pre>{answer}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
