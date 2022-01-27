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

export { updateStartedTests, updateCompletedTests, updateTotalTestsTime };
