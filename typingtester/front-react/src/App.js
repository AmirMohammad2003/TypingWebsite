import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import Base from "./components/Base";
import TypingPage from "./components/TypingPage";
import AccountHandler from "./components/AccountHandler";
import ResetPasswordPage from "./components/ResetPasswordPage";
import SuccessPage from "./components/SuccessPage";

// testContext = createContext()

const App = () => {
  return (
    <>
      <Router>
        <Routes>
          <Route path="/" element={<Base />}>
            <Route path="" element={<TypingPage />} />
            <Route path="account" element={<AccountHandler />} />
            <Route
              path="account/reset/:uidb64/:token"
              element={<ResetPasswordPage />}
            />
            <Route path="success/:type" element={<SuccessPage />} />
            <Route path="*" element={<Navigate to="/" replace="true" />} />
          </Route>
        </Routes>
      </Router>
    </>
  );
};

export default App;
