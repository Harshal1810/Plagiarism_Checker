import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [file1, setFile1] = useState(null);
  const [file2, setFile2] = useState(null);
  const [cosineSimilarity, setCosineSimilarity] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFile1Change = (e) => {
    setFile1(e.target.files[0]);
  };

  const handleFile2Change = (e) => {
    setFile2(e.target.files[0]);
  };

  const calculateSimilarity = async () => {
    try {
      setLoading(true);
      const formData = new FormData();
      formData.append('file1', file1);
      formData.append('file2', file2);

      const response = await axios.post('http://127.0.0.1:8000/plag_checker', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log(response.data)
      setCosineSimilarity(response.data);
    } catch (error) {
      console.error('Error calculating similarity:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="container p-4 bg-light rounded shadow">
        <h1 className="text-center mb-4">Plagiarism Checker</h1>
        <div className="mb-3">
          <label htmlFor="file1" className="form-label">
            Upload Text Document 1
          </label>
          <input
            type="file"
            className="form-control"
            id="file1"
            onChange={handleFile1Change}
          />
        </div>
        <div className="mb-3">
          <label htmlFor="file2" className="form-label">
            Upload Text Document 2
          </label>
          <input
            type="file"
            className="form-control"
            id="file2"
            onChange={handleFile2Change}
          />
        </div>
        <button className="btn btn-primary w-100" onClick={calculateSimilarity}>
          Calculate Similarity
        </button>
        {loading && (
          <div className="mt-3 d-flex justify-content-center">
            <div className="spinner-border text-primary" role="status"></div>
          </div>
        )}
        {cosineSimilarity !== null && (
          <p className="mt-3 text-center">
            Cosine Similarity: {cosineSimilarity}
          </p>
        )}
      </div>
    </div>
  );
}

export default App;
