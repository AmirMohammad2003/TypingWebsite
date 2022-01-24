import React, { useState, useEffect, useReducer } from "react";
import { Container } from "@mui/material";
import { Outlet } from "react-router-dom";
import { IconButtonLink } from "./smallComponents";
import { isAuthenticated } from "../lookups/lookups";

export default () => {
  const [authenticated, setAuthenticated] = useState([false, null]);
  const [any, forceUpdate] = useReducer((num) => num + 1, 0);
  useEffect(async () => {
    setAuthenticated(await isAuthenticated());
    forceUpdate();
  }, []);
  // console.log(authenticated);
  return (
    <>
      <Container maxWidth="lg">
        <div className="wrapper-flex">
          <div className="center-content">
            <div id="topSide">
              <div id="logo">TypingTester</div>
              <div id="menu">
                <IconButtonLink to="/" iconClass="keyboard" />
                <IconButtonLink to="#" iconClass="crown" />
                <IconButtonLink to="#" iconClass="info" />
                <IconButtonLink
                  to="/account"
                  iconClass="user"
                  optionalText={authenticated[0] ? authenticated[1] : ""}
                />
              </div>
            </div>
            <div id="middleSide">
              <Outlet />
            </div>

            <div id="bottomSide">{/* TODO */}</div>
          </div>
        </div>
      </Container>
    </>
  );
};
