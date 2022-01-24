import React, { useState, useEffect /*, useReducer*/ } from "react";
import { Container } from "@mui/material";
import { Outlet } from "react-router-dom";
import { IconButtonLink } from "./smallComponents";
import { isAuthenticated } from "../lookups/lookups";
import { handleLogoutSubmission } from "../lookups/auth";

export default () => {
  const [authenticated, setAuthenticated] = useState([false, null]); // authenticated[1] : username
  // const [any, forceUpdate] = useReducer((num) => num + 1, 0);
  useEffect(async () => {
    setAuthenticated(await isAuthenticated());
    // forceUpdate();
  }, []);
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
                {authenticated[0] && (
                  <IconButtonLink
                    to="#"
                    iconClass="sign-out-alt"
                    onClickCallback={(e) => {
                      e.preventDefault();
                      handleLogoutSubmission();
                      setAuthenticated([false, null]);
                    }}
                  />
                )}
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
