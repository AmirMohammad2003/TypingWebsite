import React, { useState, useRef, useEffect, useReducer } from "react";
import { CircularProgress } from "@mui/material";
import getQuote from "../lookups/lookups";
import { calculateWpmCpm, calculateAccuracy } from "../util";

import Word from "./Word";

import { IconButtonWithPopup } from "./smallComponents";

export default () => {
  const [typingState, setTypingState] = useState([[], {}]);
  const [dontFocus, setDontfocus] = useState(false);
  const [any, forceUpdate] = useReducer((num) => num + 1, 0);

  const words_typed = useRef(0);
  const start_time = useRef(0);
  const end_time = useRef(0);
  const status = useRef(0); // 0 --> not started, 1 --> has started, 2 --> ended
  const letters_typed = useRef(0); // including bad ones O_o, excluding spaces
  const mainInput = useRef(null);
  const errors = useRef(0);

  useEffect(async () => {
    let quote = await getQuote().then((_res) => JSON.parse(_res));
    setTimeout(() => {
      let ts = [];
      // console.log(quote);
      for (let i = 0; i < quote["words"].length; i++) {
        ts.push("");
      }
      // console.log(ts);
      setTypingState([ts, quote]);
    }, 1000);
  }, []);

  useEffect(() => {
    mainInput.current.focus();
  }, [mainInput]);

  const handleTyping = (e) => {
    var end = 0;
    if (status.current === 0) {
      status.current = 1;
      start_time.current = new Date().getTime() / 1000;
    }
    let value = e.target.value;
    let newState = typingState;
    if (value.charAt(value.length - 1) === " ") {
      if (value.length === 1) {
        e.target.value = "";
      } else {
        words_typed.current += 1;

        e.target.value = "";
        if (words_typed.current === typingState[1]["words"].length) {
          end = 1;
        }
      }
      // letters_typed.current = 0;
    } else {
      if (
        words_typed.current + 1 === typingState[1]["words"].length &&
        value === typingState[1]["words"][words_typed.current]
      ) {
        newState[0][words_typed.current] = value;
        letters_typed.current += 1;
        words_typed.current += 1;
        e.target.value = "";
        end = 1;
      } else {
        if (value.length > newState[0][words_typed.current].length) {
          letters_typed.current += 1;
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
        console.log(letters_typed.current);
      }
      // letters_typed.current = value.length;
      setTypingState(newState);
    }

    if (end) {
      console.log("Dont focus enabled");
      mainInput.current.blur();
      mainInput.current.disabled = true;
      status.current = 2;
      setDontfocus(true);
      end_time.current = new Date().getTime() / 1000;
    }
    // console.log(words_typed.current);
    forceUpdate();
  };

  const renderResults = () => {
    let [cpm, wpm] = calculateWpmCpm(
      start_time.current,
      end_time.current,
      letters_typed.current - errors.current
    );
    let acc = calculateAccuracy(letters_typed.current, errors.current);
    // console.log(cpm);
    // console.log(wpm);
    // console.log(acc);
    console.log("LettersTyped: " + letters_typed.current);
    console.log("Errors: " + errors.current);
    return (
      <>
        <div id="detail-board" className="popup-animation">
          <div className="detail">WPM: {wpm}</div>&nbsp;&nbsp;
          <div className="detail">CPM: {cpm}</div>&nbsp;&nbsp;
          <div className="detail">ACC: {acc}%</div>&nbsp;&nbsp;
          <div className="detail">
            Time:{" "}
            {(end_time.current - start_time.current).toFixed(2).toString()}s
          </div>
        </div>
        <div className="center-flex">
          <IconButtonWithPopup
            iconClass="fa-rotate-right"
            popupText="Refresh Test"
          />
        </div>
      </>
    );
  };

  const renderDetails = () => {
    return (
      <>
        <div id="detail-board" className={status.current === 0 ? "hidden" : ""}>
          <div className="detail">
            {words_typed.current}/{typingState[1]["words"].length}
          </div>
          &nbsp;&nbsp;
          <div className="detail">Errors: {errors.current}</div>
        </div>
      </>
    );
  };

  const renderWords = (words) => {
    return (
      <>
        <div
          id="word-wrapper"
          className="popup-animation"
          style={{ color: "#616161" }}
        >
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
  };

  const renderTestingArea = (words) => {
    if (words !== undefined) {
      return (
        <>
          {renderDetails()}
          {renderWords(words)}
          <br />
          <div className="center-flex" style={{ height: "16px" }}>
            {/* <a href="/" className="popup">
              <i className="fas fa-rotate-right btn-generic"></i>
              <span className="popuptext" id="myPopup">
                Refresh Test
              </span>
            </a> */}
            <IconButtonWithPopup
              iconClass="fa-rotate-right"
              popupText="Refresh Test"
            />
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
      {(status.current === 2 && renderResults(typingState[1]["words"])) ||
        (typingState[1] && renderTestingArea(typingState[1]["words"])) || (
          <div className="center-flex">
            <CircularProgress />
          </div>
        )}
      <br />
    </>
  );
};
