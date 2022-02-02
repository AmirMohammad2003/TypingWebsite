import React from "react";
import { useNavigate } from "react-router-dom";

const IconButtonWithPopup = ({
  to,
  iconClass,
  popupText,
  onClickCallback = (e) => {},
}) => {
  const navigate = useNavigate();
  return (
    <>
      <a
        style={{ cursor: "pointer" }}
        className="popup"
        onClick={(e) => {
          onClickCallback(e);
          if (to !== "#") navigate(to);
          e.preventDefault();
        }}
      >
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
  const navigate = useNavigate();
  return (
    <a
      style={{ cursor: "pointer" }}
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

const ResultBox = ({ _key, value }) => {
  return (
    <>
      <div className="detail">
        <div className="result-key">{_key}</div>
        <div className="result-value">{value}</div>
      </div>
    </>
  );
};

const DetailBox = ({ _key, value }) => {
  return (
    <>
      <div className="detail">
        <div className="detail-key">{_key}</div>
        <div className="detail-value">{value}</div>
      </div>
    </>
  );
};

export { IconButtonWithPopup, IconButtonLink, ResultBox };
