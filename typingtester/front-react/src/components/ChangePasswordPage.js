import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Alert, Container } from "@mui/material";
import { handleChangePassword } from "../lookups/auth";
export default () => {
  const [errors, setErrors] = useState([]);
  // const [info, setInfo] = useState([]);

  const navigate = useNavigate();

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
            handleChangePassword(
              e,
              (errors) => {
                setErrors(errors);
              },
              (location) => {
                // window.location.href = location;
                navigate(location);
              },
              "/success/passwordChanged"
            );
            e.preventDefault();
          }}
        >
          <p style={{ color: "#f5e6c8", fontSize: "18pt" }}>
            Change Your Password
          </p>
          <br />
          <input
            type="password"
            className="input-generic"
            placeholder="Old Password"
            name="old_password"
          />
          <br />
          <br />
          <br />
          <input
            type="password"
            className="input-generic"
            placeholder="New Password"
            name="new_password1"
          />
          <br />
          <br />
          <input
            type="password"
            className="input-generic"
            placeholder="Confirm Your password"
            name="new_password2"
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
