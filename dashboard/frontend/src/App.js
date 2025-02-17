import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Dashboard from "./Dashboard";
import DetailsPage from "./DetailsPage";  // Assuming you create a DetailsPage component

function App() {
  return (
    <Router>
      <div className="App">
        <h1 style={{ textAlign: "center", color: "#fff" }}>Finance Dashboard</h1>      
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/details/:category" element={<DetailsPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;