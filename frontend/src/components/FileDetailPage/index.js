import { useLocation, useParams } from "react-router-dom";
const FileDetailPage = () => {
  const location = useLocation();
  const { index } = useParams();
  const { data, file_name, file_size } = location.state || {};
  return (
    <div className="container mx-auto p-6">
      <h1>File Details</h1>
      <h3>{file_name}</h3>
      <p>Size: {file_size} bytes</p>
      <div>
        {data ? (
          data.map((item, idx) => (
            <div key={idx} className="border p-4 my-4">
              <p>Filename: {item.filename}</p>
              <p>Timestamp: {item.timestamp}</p>
              <p>Certifying Center: {item.certifying_center}</p>
              <p>Date: {item.date}</p>
              <p>Recipient: {item.recipient}</p>
              <p>Amount: {item.amount}</p>
              <p>Status: {item.status}</p>
            </div>
          ))
        ) : (
          <p>No data available</p>
        )}
      </div>
    </div>
  );
};

export default FileDetailPage;
