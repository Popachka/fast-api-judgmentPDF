import React, { createContext, useState } from "react";

export const FileContext = createContext();

export const FileProvider = ({ children }) => {
  const [uploadedFiles, setUploadedFiles] = useState([]);

  return (
    <FileContext.Provider value={{ uploadedFiles, setUploadedFiles }}>
      {children}
    </FileContext.Provider>
  );
};
