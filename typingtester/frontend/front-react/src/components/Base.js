import React from "react";
import { Container } from "@mui/material";

export default () => {
  return (
    <>
      <Container maxWidth="lg" style={{ backgroundColor: "white" }}>
        <div className="wrapper-flex">
          <div className="center-content">
            <div id="topSide">
              <div id="logo">TypingTester</div>
              <div id="menu">
                <a href="/" className="button-link">
                  <i className="fas fa-keyboard"></i>
                </a>
                <a href="#" className="button-link">
                  <i className="fas fa-crown"></i>
                </a>
                <a href="#" className="button-link">
                  <i className="fas fa-info"></i>
                </a>
                <a href="/account" className="button-link">
                  <i className="fas fa-user"></i>
                </a>
              </div>
            </div>
            <div id="middleSide">item 2</div>
            <div id="bottomSide">item 3</div>
          </div>
        </div>
      </Container>
    </>
  );
};
