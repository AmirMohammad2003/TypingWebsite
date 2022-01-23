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

const IconButtonLink = ({ to, iconClass }) => {
  return (
    <a href={to} className="button-link">
      <i className={`fa-solid fa-${iconClass}`}></i>
    </a>
  );
};

export { IconButtonWithPopup, IconButtonLink };
