import { memo } from 'react';

const Word = memo(({ word, wordState, cursor }) => {
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
});

export default Word;
