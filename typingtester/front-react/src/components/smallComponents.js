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
  return (
    <a
      href={to}
      className="button-link"
      onClick={(e) => {
        onClickCallback(e);
      }}
    >
      <i className={`fa-solid fa-${iconClass}`}></i>
      &nbsp;
      {optionalText}
    </a>
  );
};

export { IconButtonWithPopup, IconButtonLink };
