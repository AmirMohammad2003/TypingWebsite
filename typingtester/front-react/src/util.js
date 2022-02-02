const calculateWpmCpm = (start, end, charsTyped) => {
  let time = end - start;
  let cpm = charsTyped / (time / 60);
  let wpm = cpm / 5;
  return [Math.round(cpm), Math.round(wpm)];
};

const calculateAccuracy = (charsTyped, errors) => {
  return 100 - Math.round((errors / charsTyped) * 100);
};

const convertDateToFormattedTime = (_date) => {
  const monthNames = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];

  let date = new Date(_date);
  let hours = date.getHours();
  let minutes = date.getMinutes();

  hours = hours < 10 ? `0${hours}` : hours;
  minutes = minutes < 10 ? `0${minutes}` : minutes;

  let year = date.getFullYear();
  let month = monthNames[date.getMonth()];
  let day = date.getDate();

  month = month < 10 ? `0${month}` : month;

  let dateString = `${day} ${month} ${year}`;
  let timeString = `${hours}:${minutes}`;
  return dateString + " " + timeString;
};

//convert seconds to hh:mm:ss format
const convertSecondsToTime = (seconds) => {
  let hours = Math.floor(seconds / 3600);
  let minutes = Math.floor((seconds - hours * 3600) / 60);
  let secondsLeft = seconds - hours * 3600 - minutes * 60;

  minutes = minutes < 10 ? `0${minutes}` : minutes;
  secondsLeft = secondsLeft < 10 ? `0${secondsLeft}` : secondsLeft;

  return hours + ":" + minutes + ":" + secondsLeft;
};

export {
  calculateWpmCpm,
  calculateAccuracy,
  convertDateToFormattedTime,
  convertSecondsToTime,
};
