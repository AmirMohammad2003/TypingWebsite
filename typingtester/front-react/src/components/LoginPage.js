import React, { useState, useRef } from "react";
import { Grid, Alert, Container, Button } from "@mui/material";
import {
  handleRegistrationSubmission,
  handleLoginSubmission,
  handleResetPassword,
  handleResendRequestForPasswordReset,
} from "../lookups/auth";

const LoginPage = () => {
  const [errors, setErrors] = useState([]);
  const [info, setInfo] = useState([[], null]);
  const resendButton = useRef();
  return (
    <>
      <Container maxWidth="sm">
        {/* TODO make this guy a component */}
        {errors.map((errorMessage, index) => (
          <Alert severity="error" key={index} variant="filled">
            {errorMessage}
          </Alert>
        ))}
        {info[0].map((infoMessage, index) => (
          <Alert
            severity="info"
            key={index}
            variant="filled"
            action={
              info[1] !== null && (
                <Button
                  ref={resendButton}
                  color="inherit"
                  size="small"
                  onClick={() => {
                    if (info[1] === "reset") {
                      handleResendRequestForPasswordReset();
                    }
                    resendButton.current.disabled = true;
                    setTimeout(() => {
                      resendButton.current.disabled = false;
                    }, 60000);
                  }}
                >
                  RESEND
                </Button>
              )
            }
          >
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
                  setInfo([info, "reset"]);
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
                  window.location.replace = "/";
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
            <br />
            <div style={{ width: "20em" }} align="left">
              <a
                onClick={(e) => {
                  e.preventDefault();
                  const email = prompt("Enter your email address:");
                  handleResetPassword(
                    email,
                    (errors) => {
                      setErrors(errors);
                    },
                    (info) => {
                      setInfo([info, null]);
                    }
                  );
                }}
                style={{ cursor: "pointer" }}
              >
                forgot your password?
              </a>
              <br />
              <label style={{ color: "#6f6c6c" }}>
                {/* i may customize this field in future */}
                <input
                  className="margin-top-26"
                  type="checkbox"
                  name="remember_me"
                  id="remember_me"
                />
                Remember me
              </label>
            </div>
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
