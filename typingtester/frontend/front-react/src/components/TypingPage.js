import React, { useState, useRef, useEffect, useReducer } from "react";
import { CircularProgress } from "@mui/material";
import getQuote from "../lookups/lookups";

const Word = ({ word, wordState, cursor }) => {
  console.log(wordState);
  let cursor_index = -2;
  if (cursor === true) {
    cursor_index = word.length === wordState.length ? -1 : wordState.length;
  }
  return (
    <div className="word">
      {[...word].map((letter, index) => {
        let color = "";
        if (index < wordState.length) {
          color =
            word.charAt(index) === wordState.charAt(index)
              ? "correctChar"
              : "wrongChar";
        }
        return (
          <span
            key={index}
            className={color + (index === cursor_index ? " cursor" : "")}
          >
            {letter}
          </span>
        );
      })}
      {(wordState.length > word.length && (
        <>
          {[...wordState].map((letter, index) => {
            if (index >= word.length) {
              return (
                <span key={index} className="extra">
                  {letter}
                </span>
              );
            }
          })}
          <span className={cursor ? "cursor" : ""}>&nbsp;</span>
        </>
      )) || <span className={cursor_index === -1 ? "cursor" : ""}>&nbsp;</span>}
    </div>
  );
};

export default () => {
  const [typingState, setTypingState] = useState([[], {}]);
  const [dontFocus, setDontfocus] = useState(false);
  const [any, forceUpdate] = useReducer((num) => num + 1, 0);

  const words_typed = useRef(0);
  const [status, setStatus] = useRef(0); // 0 --> not started, 1 --> has started, 2 --> ended
  // const letters_typed = useRef(0);
  const mainInput = useRef(null);
  const errors = useRef(0);

  useEffect(async () => {
    let quote = await getQuote().then((_res) => JSON.parse(_res));
    setTimeout(() => {
      let ts = [];
      console.log(quote);
      for (let i = 0; i < quote["words"].length; i++) {
        ts.push("");
      }
      console.log(ts);
      setTypingState([ts, quote]);
    }, 1000);
  }, []);

  useEffect(() => {
    mainInput.current.focus();
  }, [mainInput]);

  const handleTyping = (e) => {
    if (status === 0)
    let value = e.target.value;
    let newState = typingState;
    if (value.charAt(value.length - 1) === " ") {
      if (value.length === 1) {
        e.target.value = "";
      } else {
        words_typed.current = words_typed.current + 1;
        e.target.value = "";
        if (words_typed.current === typingState[1]["words"].length) {
          console.log("Dont focus enabled");
          mainInput.current.blur();
          mainInput.current.disabled = true;
          setDontfocus(true);
        }
      }
      // letters_typed.current = 0;
    } else {
      if (
        words_typed.current + 1 === typingState[1]["words"].length &&
        value === typingState[1]["words"][words_typed.current]
      ) {
        newState[0][words_typed.current] = value;
        words_typed.current = words_typed.current + 1;
        e.target.value = "";
        console.log("Dont focus enabled 2");
        mainInput.current.blur();
        mainInput.current.disabled = true;
        setDontfocus(true);
      } else {
        if (value.length > newState[0][words_typed.current].length) {
          if (value.length > newState[1]["words"][words_typed.current].length) {
            errors.current += 1;
          } else if (
            value.charAt(value.length - 1) !==
            newState[1]["words"][words_typed.current].charAt(value.length - 1)
          ) {
            errors.current += 1;
          }
        }
        newState[0][words_typed.current] = value;
      }
      // letters_typed.current = value.length;
      setTypingState(newState);
    }
    console.log(words_typed.current);
    forceUpdate();
  };

  const renderWords = (words) => {
    if (words !== undefined) {
      return (
        <>
          <div id="detail-board">
            <div className="detail">
              {words_typed.current}/{typingState[1]["words"].length}
            </div>
            &nbsp;&nbsp;
            <div className="detail">Errors: {errors.current}</div>
          </div>
          <div id="word-wrapper" style={{ color: "#616161" }}>
            {words.map((word, index) => (
              <Word
                key={index}
                word={word}
                wordState={typingState[0][index]}
                cursor={words_typed.current === index}
              />
            ))}
          </div>
        </>
      );
    }
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
      <br />
      {(typingState[1] && renderWords(typingState[1]["words"])) || (
        <div className="center-flex">
          <CircularProgress />
        </div>
      )}
    </>
  );
};
