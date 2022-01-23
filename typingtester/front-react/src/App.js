import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Base from "./components/Base";
import TypingPage from "./components/TypingPage";

// testContext = createContext()

const App = () => {
  return (
    <>
      <Router>
        <Routes>
          <Route path="/" element={<Base />}>
            <Route path="" element={<TypingPage />} />
            {/* <Route path="account" /> */}
            <Route path="*" element={<Navigate to="/" replace="true" />} />
          </Route>
        </Routes>
      </Router>
    </>
  );
};

export default App;
