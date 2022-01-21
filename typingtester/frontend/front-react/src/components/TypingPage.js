import React, { useState, useRef, useEffect } from "react";

export default () => {
  const [typingState, setTypingState] = useState("");
  const [dontFocus, setDontfocus] = useState(false);
  const mainInput = useRef(null);
  useEffect(() => {
    mainInput.current.focus();
  }, [mainInput]);
  const handleTyping = (e) => {
    setTypingState(e.target.value);
  };
  return (
    <>
      <input
        ref={mainInput}
        type="text"
        id="mainInput"
        autoComplete="off"
        autoCapitalize="off"
        autoCorrect="off"
        onBlur={(e) => {
          dontFocus ? e.target.blur() : e.target.focus();
        }}
        onFocus={(e) => {
          dontFocus ? e.target.blur() : e.target.focus();
        }}
        onChange={handleTyping}
      />
      <p>This is the typing page.</p>
      <p>{typingState}</p>
    </>
  );
};
