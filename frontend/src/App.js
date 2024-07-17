import Card from "./components/Card";
import Header from "./components/Header";
import FileInput from "./components/FileInput";
import Footer from "./components/Footer";
import React, { useState, useContext } from "react";
import { FileContext } from "./context/FileContext";
import { Link } from "react-router-dom";
function App() {
  const { uploadedFiles, setUploadedFiles } = useContext(FileContext);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const openModal = () => {
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };
  return (
    <div className="App fh-full ">
      <Header />
      <div className="container p-6 mx-auto flex-col h-screen">
        <h1 className="mt-20 text-4xl">О нашем сервисе</h1>
        <div className="mt-5 border-double border-4 border-indigo-600">
          <div className="p-5">
            Наш сайт создан для извлечения информации из PDF-файлов судебных
            решений. На данный момент скрипт поддерживает только определённый
            формат документов
            <span onClick={openModal} className="text-blue-500 underline cursor-pointer">
              (пример)
            </span>
            . <br></br>
            <br></br>После загрузки файла автоматически создаётся карточка с
            полной информацией о содержимом. <br></br>
            <br></br>Чтобы протестировать работу сервиса, вы можете загрузить
            примеры документов из нашего архива:
            <a href="https://www.kaggle.com/datasets/simaca/judgmentreasonsrus" className="text-blue-500 underline">База данных документов</a>.
          </div>
          {isModalOpen && (
            <div className="fixed inset-0 bg-gray-600 bg-opacity-75 flex items-center justify-center overflow-y-auto">
              <div className="bg-white p-5 rounded shadow-lg">
                <img
                  src="Example.png"
                  alt="Example document screenshot"
                  className="mb-4 "
                />
                <button
                  className="px-4 py-2 bg-red-500 text-white rounded"
                  onClick={closeModal}
                >
                  Close
                </button>
              </div>
            </div>
          )}
        </div>
        <FileInput setUploadedFiles={setUploadedFiles} />
        <h2 className="mt-10 text-4xl">Ваши файлы</h2>
        <div className="my-10 p-3 border-solid border-2 border-blue-300 grid grid-cols-4 grid-rows-2 gap-2 ">
          {uploadedFiles.map((file, index) => (
            <Link
              to={`/file/${index}`}
              state={{
                data: file.data,
                file_name: file.file_name,
                file_size: file.file_size,
              }}
            >
              <Card
                key={index}
                data={file.data}
                file_name={file.file_name}
                file_size={file.file_size}
                index={index}
              />
            </Link>
          ))}
        </div>
        <Footer />
      </div>
    </div>
  );
}

export default App;
