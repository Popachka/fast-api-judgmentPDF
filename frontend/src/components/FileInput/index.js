import React, { useState, useRef } from "react";

const FileInput = ({ setUploadedFiles }) => {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const fileInputRef = useRef(null);

  const handleFileChange = (event) => {
    setSelectedFiles([...event.target.files]);
  };
  const handleFileUpload = async () => {
    if (selectedFiles.length === 0) {
      alert("Please select files first!");
      return;
    }
    // Сброс значения поля ввода файлов
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
    const formData = new FormData();
    selectedFiles.forEach((file) => {
      formData.append("files", file);
    });

    try {
      const response = await fetch("https://judgmentfiles.online/api/upload-pdf", {
        method: "POST",
        body: formData,
      });
      const result = await response.json();
      setUploadedFiles(result.files);
    } catch (error) {
      console.error("Error uploading files:", error);
    }
  };
  return (
    <div className="mt-20 p-10 ">
      <label
        class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
        for="multiple_files"
      >
        Загрузите один или несколько файлов
      </label>
      <input
        ref={fileInputRef}
        class="block w-full text-sm text-gray-900 border border-gray-300
       rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none
        dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"
        id="multiple_files"
        type="file"
        onChange={handleFileChange}
        multiple
      ></input>
      <button
        className="mt-4 px-4 py-2 bg-blue-500 text-white rounded"
        onClick={handleFileUpload}
      >
        Отправить
      </button>
    </div>
  );
};

export default FileInput;
