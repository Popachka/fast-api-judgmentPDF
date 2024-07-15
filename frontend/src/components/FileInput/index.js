import React, { useState } from "react";
import axios from "axios";

const FileInput = ({ setUploadedFiles }) => {
  const [selectedFiles, setSelectedFiles] = useState([]);

  const handleFileChange = (event) => {
    setSelectedFiles([...event.target.files]);
  };
  const handleFileUpload = async () => {
    if (selectedFiles.length === 0) {
      alert("Please select files first!");
      return;
    }

    const formData = new FormData();
    selectedFiles.forEach(file => {
      formData.append('files', file);
    });

    try {
      const response = await fetch('http://localhost:8000/upload-pdf/', {
        method: 'POST',
        body: formData,
      });
      const result = await response.json();
      setUploadedFiles(result.files)
      console.log(result);
    } catch (error) {
      console.error('Error uploading files:', error);
    }
  };
  return (
    <div className="mt-5 flex ">
      <div className="flex items-center justify-center w-full px-60 py-4">
        <label
          htmlFor="dropzone-file"
          className="w-full flex flex-col items-center justify-center border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 dark:hover:bg-gray-800 dark:bg-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:hover:border-gray-500 dark:hover:bg-gray-600"
        >
          <div className="flex flex-col items-center justify-center pt-5 pb-6">
            <svg
              className="w-8 h-8 mb-4 text-gray-500 dark:text-gray-400"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 20 16"
            >
              <path
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"
              />
            </svg>
            <p className="mb-2 text-sm text-gray-500 dark:text-gray-400">
              <span className="font-semibold">Click to upload</span> or drag and
              drop
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              Only PDF (Max 2MB)
            </p>
          </div>
          <input
            id="dropzone-file"
            type="file"
            multiple
            className="hidden"
            onChange={handleFileChange}
          />
        </label>
        <button
          onClick={handleFileUpload}
          className="mt-2 px-4 py-2 bg-blue-500 text-white rounded"
        >
          Upload File
        </button>
      </div>
    </div>
  );
};

export default FileInput;
