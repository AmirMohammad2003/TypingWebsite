import React from "react";
import { useParams, useNavigate } from "react-router-dom";

export default () => {
  const params = useParams();
  const navigate = useNavigate();
  // TODO going to change how this guy works i don't like to hard code anything in the frontend

  return (
    <>
      <div
        className="center-flex"
        style={{ color: "#f5e6c8", fontSize: "18pt" }}
      >
        {(params.type === "emailVerified" && (
          <p>
            Your Email Address Has been Verified, Please navigate to the{" "}
            <a
              href="#"
              onClick={(e) => {
                navigate("/account");
                e.preventDefault();
              }}
            >
              Login page
            </a>{" "}
            to login into your account.
          </p>
        )) ||
          (params.type === "passwordResetDone" && (
            <p>
              Your Password Reset Successfully please go back to{" "}
              <a
                href="#"
                onClick={(e) => {
                  navigate("/account");
                  e.preventDefault();
                }}
              >
                Login Page
              </a>{" "}
              and login to your account.
            </p>
          )) ||
          (params.type === "passwordChanged" && (
            <p>Your Password Changed Successfully.</p>
          )) ||
          navigate("/")}
      </div>
    </>
  );
};
