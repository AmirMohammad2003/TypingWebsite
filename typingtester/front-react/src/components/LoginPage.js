import React, { useState } from "react";
import { Grid, Alert, Container } from "@mui/material";
import { getCsrfToken } from "../lookups/lookups";
import { useNavigate } from "react-router-dom";

const handleLoginSubmission = async (
  e,
  updateErrorsCallback,
  successCallback
) => {
  updateErrorsCallback([]);
  e.preventDefault();
  if (e.target[0].value.trim() === "" || e.target[1].value.trim() === "") {
    return;
  }
  let data = new FormData(e.target);

  const requestOptions = {
    method: "POST",
    headers: {
      "X-CSRFToken": await getCsrfToken(),
      Accept: "application/json",
      HTTP_X_REQUESTED_WITH: "XMLHttpRequest",
      "X-Requested-With": "XMLHttpRequest",
    },
    credentials: "include",
    body: data,
  };
  fetch("/auth/login/", requestOptions)
    .then((response) => response.json())
    .then((data) => {
      if (data["success"] === "true") {
        console.log(data["username"]);
        localStorage.setItem("username", data["username"]);
        successCallback();
      } else if (data["success"] === "false") {
        updateErrorsCallback([data["message"]]);
      }
    })
    .catch((error) => console.error(error));
};

const handleRegistrationSubmission = async (
  e,
  updateErrorsCallback,
  successCallback
) => {
  updateErrorsCallback([]);
  e.preventDefault();
  if (
    e.target[0].value.trim() === "" ||
    e.target[1].value.trim() === "" ||
    e.target[2].value.trim() === "" ||
    e.target[3].value.trim() === ""
  ) {
    return;
  }

  let data = new FormData(e.target);

  const requestOptions = {
    method: "POST",
    headers: {
      "X-CSRFToken": await getCsrfToken(),
      Accept: "application/json",
      HTTP_X_REQUESTED_WITH: "XMLHttpRequest",
      "X-Requested-With": "XMLHttpRequest",
    },
    credentials: "include",
    body: data,
  };
  fetch("/auth/register/", requestOptions)
    .then((response) => response.json())
    .then((data) => {
      if (data["success"] === "true") {
        console.log(data["username"]);
        localStorage.setItem("username", data["username"]);
        successCallback();
      } else if (data["success"] === "false") {
        updateErrorsCallback([data["errors"]]);
      }
    })
    .catch((error) => console.log(error));
};

const LoginPage = (props) => {
  const navigate = useNavigate();

  const [errors, setErrors] = useState([]);
  console.log(errors);
  return (
    <>
      <Container maxWidth="sm">
        {errors.map((errorMessage, index) => (
          <Alert
            severity="error"
            key={index}
            variant="filled"
            onClose={(e) => {
              e.target.parentNode.parentNode.parentNode.parentNode.style.display =
                "none";
            }}
          >
            {errorMessage}
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
                () => {
                  navigate("/");
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
                  navigate("/");
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
