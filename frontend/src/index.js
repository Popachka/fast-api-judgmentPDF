import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import FileDetailPage from "./components/FileDetailPage";
const router = createBrowserRouter([
    {
        path:'/',
        element: <App />
    },
    {
        path: '/file/:fileId',
        element: <FileDetailPage />
    }
])
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
    <RouterProvider router={router} />
);
