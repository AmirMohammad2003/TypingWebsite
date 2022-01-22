import React, { useState, useRef, useEffect, useReducer } from "react";
import { CircularProgress } from "@mui/material";
import getQuote from "../lookups/lookups";

const Word = ({ word, wordState, cursor }) => {
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
      <span className={cursor_index === -1 ? " cursor" : ""}>&nbsp;</span>
    </div>
  );
};

export default () => {
  const [typingState, setTypingState] = useState([[], {}]);
  const [dontFocus, setDontfocus] = useState(false);
  const [any, forceUpdate] = useReducer((num) => num + 1, 0);
  const words_typed = useRef(0);
  const letters_typed = useRef(0);
  const mainInput = useRef(null);

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
          setDontfocus(true);
        }
      }
      letters_typed.current = 0;
    } else {
      if (
        words_typed.current + 1 === typingState[1]["words"].length &&
        value === typingState[1]["words"][words_typed.current]
      ) {
        newState[0][words_typed.current] = value;
        words_typed.current = words_typed.current + 1;
        console.log("Dont focus enabled _2_");
        mainInput.current.blur();
        setDontfocus(true);
      } else {
        newState[0][words_typed.current] = value;
      }
      letters_typed.current = value.length;
      setTypingState(newState);
    }
    console.log(words_typed.current);
    forceUpdate();
  };

  const renderWords = (words) => {
    // TODO: implement the cursor
    if (words !== undefined) {
      return (
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
      <div id="detail-board">
        <div> {/* TODO: words typed */}</div>
      </div>
      <br />
      {(typingState[1] && renderWords(typingState[1]["words"])) || (
        <div className="center-flex">
          <CircularProgress />
        </div>
      )}
    </>
  );
};
