import React from "react";
const Card = ({ data, file_name, file_size, index }) => {
  return (
    <div
      className="border border-gray-300 p-3 rounded overflow-hidden"
    >
      <>
        <p>Название файла: {file_name}</p>
        <p>Размер файла: {file_size} bytes</p>
        {/* Другая полная информация о файле */}
      </>
    </div>
  );
};

export default Card;
