import React, { useEffect, useState } from "react";
import LoginPage from "./LoginPage";
import Profile from "./Profile";
import { CircularProgress } from "@mui/material";
import { isAuthenticatedStrict } from "../lookups/lookups";

export default () => {
  const [authenticated, setAuthenticated] = useState(["unknown", null]);
  useEffect(() => {
    (async () => {
      setAuthenticated(await isAuthenticatedStrict());
    })();
  }, []);
  if (authenticated[0] === true) {
    return <Profile username={authenticated[1]} />;
  } else if (authenticated[0] === false) {
    return <LoginPage />;
  } else {
    return (
      <div className="center-flex">
        <CircularProgress />
      </div>
    );
  }
};
