import React from "react";
import { useNavigate } from "react-router-dom";

const IconButtonWithPopup = ({ iconClass, popupText }) => {
  return (
    <>
      <a href="/" className="popup">
        <i className={`fa-solid ${iconClass} btn-generic`}></i>
        <span className="popuptext">{popupText}</span>
      </a>
    </>
  );
};

const IconButtonLink = ({
  to,
  iconClass,
  optionalText = "",
  onClickCallback = (e) => {},
}) => {
  let navigate = useNavigate();
  return (
    <a
      href={to}
      className="button-link"
      onClick={(e) => {
        onClickCallback(e);
        if (to !== "#") navigate(to);
        e.preventDefault();
      }}
    >
      <i className={`fa-solid fa-${iconClass}`}></i>
      &nbsp;
      {optionalText}
    </a>
  );
};

export { IconButtonWithPopup, IconButtonLink };
