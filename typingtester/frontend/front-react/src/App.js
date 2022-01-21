import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Base from "./components/Base";

const App = () => {
  return (
    <>
      <Router>
        <Routes>
          <Route path="/" element={<Base />}>
            {/* <Route path="" /> */}
            {/* <Route path="account" /> */}
          </Route>
        </Routes>
      </Router>
    </>
  );
};

export default App;
