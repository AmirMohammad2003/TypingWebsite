import { getCsrfToken } from "./lookups";

const updateStartedTests = async () => {
  const requestOptions = {
    method: "POST",
    headers: {
      "X-CSRFtoken": await getCsrfToken(),
      Accept: "application/json",
    },
  };

  fetch("/api/started-test/", requestOptions)
    .then((response) => response.json())
    .then((data) => {
      if (data["success"] === true) {
        console.log("Successfully updated started test");
      }
    })
    .catch((error) => console.log(error));
};

const updateCompletedTests = async () => {
  const requestOptions = {
    method: "POST",
    headers: {
      "X-CSRFtoken": await getCsrfToken(),
      Accept: "application/json",
    },
  };

  fetch("/api/completed-test/", requestOptions)
    .then((response) => response.json())
    .then((data) => {
      if (data["success"] === true) {
        console.log("Successfully updated completed test");
      }
    })
    .catch((error) => console.log(error));
};

const updateTotalTestsTime = async (time) => {
  const requestOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFtoken": await getCsrfToken(),
      Accept: "application/json",
    },
    body: JSON.stringify({ time: time }),
  };

  fetch("/api/update-total-tests-time/", requestOptions)
    .then((response) => response.json())
    .then((data) => {
      if (data["success"] === true) {
        console.log("Successfully updated total tests time");
      }
    })
    .catch((error) => console.log(error));
};

const SendTestRecordData = async (quote_id, time, cpm, acc) => {
  const requestOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFtoken": await getCsrfToken(),
      Accept: "application/json",
    },
    body: JSON.stringify({
      time: time,
      cpm: cpm,
      acc: acc,
      quote_id: quote_id,
    }),
  };

  fetch("/api/insert-user-test/", requestOptions)
    .then((response) => response.json())
    .then((data) => {
      if (data["success"] === "true") {
        console.log("Successfully saved user test");
      } else {
        console.log("Failed to save user test", data);
      }
    });
};

export {
  updateStartedTests,
  updateCompletedTests,
  updateTotalTestsTime,
  SendTestRecordData,
};
