import React from "react";
import { useParams, useNavigate } from "react-router-dom";

export default () => {
  const params = useParams();
  const navigate = useNavigate();
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
              Login
            </a>{" "}
            page to login into your account.
          </p>
        )) ||
          navigate("/")}
      </div>
    </>
  );
};
