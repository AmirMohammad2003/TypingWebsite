import React, { useState, useEffect } from "react";
import { Grid, Alert, Container } from "@mui/material";
import { useParams } from "react-router-dom";
import { handleResetPasswordConfirmation } from "../lookups/auth";
export default () => {
  const [errors, setErrors] = useState([]);
  // const [info, setInfo] = useState([]);
  const params = useParams();

  return (
    <>
      <Container maxWidth="sm">
        {errors.map((errorMessage, index) => (
          <Alert severity="error" key={index} variant="filled">
            {errorMessage}
          </Alert>
        ))}
        {/* {info.map((infoMessage, index) => (
          <Alert severity="info" key={index} variant="filled">
            {infoMessage}
          </Alert>
        ))} */}
      </Container>
      <div className="center-flex" align="center">
        <form
          onSubmit={(e) => {
            handleResetPasswordConfirmation(
              e,
              params.uidb64,
              params.token,
              (errors) => {
                setErrors(errors);
              },
              (location) => {
                window.location.href = location;
              }
            );
            e.preventDefault();
          }}
        >
          <p style={{ color: "#f5e6c8", fontSize: "18pt" }}>
            Reset Your Password
          </p>
          <br />
          <input
            type="password"
            className="input-generic"
            placeholder="Your new Password"
            name="password1"
          />
          <br />
          <br />
          <input
            type="password"
            className="input-generic"
            placeholder="Confirm Your password"
            name="password2"
          />
          <br />
          <br />
          <input
            type="submit"
            className="input-generic"
            name="submit"
            value="Reset"
            style={{ cursor: "pointer" }}
          />
        </form>
      </div>
    </>
  );
};
