import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import { Route, Routes, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Home from "./pages/Home";
import Whitelist from "./components/Whitelist";

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/home" element={<Home></Home>} />
        <Route path="/test" element={<Whitelist></Whitelist>} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </>
  );
}

export default App;
