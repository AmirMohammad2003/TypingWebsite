const calculateWpmCpm = (start, end, charsTyped) => {
  let time = end - start;
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
