import React, { useState, useEffect } from "react";
import { Container } from "@mui/material";
import { Outlet } from "react-router-dom";
import { IconButtonLink } from "./smallComponents";
import { isAuthenticated } from "../lookups/lookups";
import { handleLogoutSubmission } from "../lookups/auth";

export default () => {
  const [authenticated, setAuthenticated] = useState([false, null]); // authenticated[1] : username
  useEffect(() => {
    (async () => {
      setAuthenticated(await isAuthenticated());
    })();
  }, []);
  return (
    <>
      <Container maxWidth="lg">
        <div className="wrapper-flex">
          <div className="center-content">
            <div id="topSide">
              <div id="logo">TypingTester</div>
              <div id="menu">
                {/* TODO fix the navigation bug */}
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
                      window.location.href = "/";
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
