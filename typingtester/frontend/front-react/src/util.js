const calculateWpmCpm = (start, end, words) => {
  let time = end - start;
  let charsTyped = words.length - 1;
  for (let word of words) {
    charsTyped += word.length;
  }

  let cpm = charsTyped / (time / 60);
  let wpm = cpm / 5;
  console.log(cpm);
  console.log(wpm);
  return [Math.round(cpm), Math.round(wpm)];
};

const calculateAccuracy = (charsTyped, errors) => {
  return 100 - Math.round((errors / charsTyped) * 100);
};

export { calculateWpmCpm, calculateAccuracy };
