import React from "react";
import { Container } from "@mui/material";
import { Outlet } from "react-router-dom";
import { IconButtonLink } from "./smallComponents";

export default () => {
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
                <IconButtonLink to="/account" iconClass="user" />
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
