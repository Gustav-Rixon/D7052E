import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import Home from "./pages/Home";
import { Route, Routes, Link } from "react-router-dom";
import { Camera } from "./pages/Camera";

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/camera" element={<Camera />} />
        <Route path="/camera/:id" element={<Camera />} />
      </Routes>
    </>
  );
}

export default App;
