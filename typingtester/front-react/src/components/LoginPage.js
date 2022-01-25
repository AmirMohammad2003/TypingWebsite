import React, { useState, useEffect } from "react";
import { Grid, Alert, Container } from "@mui/material";
// import { useNavigate } from "react-router-dom";
import {
  handleRegistrationSubmission,
  handleLoginSubmission,
} from "../lookups/auth";

const LoginPage = () => {
  // const navigate = useNavigate();
  const [errors, setErrors] = useState([]);
  const [info, setInfo] = useState([]);

  useEffect(() => {
    let message = sessionStorage.getItem("message");
    if (message) {
      setInfo([message]);
    }
  }, []);

  return (
    <>
      <Container maxWidth="sm">
        {errors.map((errorMessage, index) => (
          <Alert severity="error" key={index} variant="filled">
            {errorMessage}
          </Alert>
        ))}
        {info.map((infoMessage, index) => (
          <Alert severity="info" key={index} variant="filled">
            {infoMessage}
          </Alert>
        ))}
      </Container>
      <Grid container spacing={2}>
        <Grid item xs={12} md={6} align="center">
          <div className="center-flex" style={{ color: "#f66e0d" }}>
            <h2>Register</h2>
          </div>
          <form
            onSubmit={(e) => {
              handleRegistrationSubmission(
                e,
                (errors) => {
                  setErrors(errors);
                },
                (info) => {
                  // navigate("/");
                  // window.location.href = "/";
                  setInfo(info);
                }
              );
            }}
          >
            <input
              type="text"
              className="input-generic margin-top-26"
              placeholder="Username"
              name="username"
            />
            <br />
            <input
              type="password"
              className="input-generic margin-top-26"
              placeholder="Password"
              name="password1"
            />
            <br />
            <input
              type="password"
              className="input-generic margin-top-26"
              placeholder="Confirm Your Password"
              name="password2"
            />
            <br />
            <input
              type="email"
              className="input-generic margin-top-26"
              placeholder="E-mail"
              name="email"
            />
            <br />
            <input
              type="submit"
              value="Register"
              className="input-generic margin-top-26"
              style={{ cursor: "pointer" }}
            />
          </form>
        </Grid>
        <Grid item xs={12} md={6} align="center">
          <div className="center-flex" style={{ color: "#f66e0d" }}>
            <h2>Login</h2>
          </div>
          <form
            onSubmit={(e) => {
              handleLoginSubmission(
                e,
                (errors) => {
                  setErrors(errors);
                },
                () => {
                  // navigate("/");
                  window.location.href = "/";
                }
              );
            }}
          >
            <input
              type="text"
              className="input-generic margin-top-26"
              placeholder="Username"
              name="username"
            />
            <br />
            <input
              type="password"
              className="input-generic margin-top-26"
              placeholder="Password"
              name="password"
            />
            <br />
            <label style={{ color: "#6f6c6c" }}>
              <input
                className="margin-top-26"
                type="checkbox"
                name="remember_me"
                id="remember_me"
              />
              Remember me
            </label>
            {/* i may customize this field in future */}
            <br />
            <input
              type="submit"
              value="Login"
              className="input-generic margin-top-26"
              style={{ cursor: "pointer" }}
            />
          </form>
        </Grid>
      </Grid>
    </>
  );
};

export default LoginPage;
