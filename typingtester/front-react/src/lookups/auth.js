import { getCsrfToken, isAuthenticatedStrict } from "./lookups";

const handleLoginSubmission = async (
  e,
  updateErrorsCallback,
  successCallback
) => {
  updateErrorsCallback([]);
  e.preventDefault();
  if (e.target[0].value.trim() === "" || e.target[1].value.trim() === "") {
    return;
  }
  let data = new FormData(e.target);

  const requestOptions = {
    method: "POST",
    headers: {
      "X-CSRFToken": await getCsrfToken(),
      Accept: "application/json",
      HTTP_X_REQUESTED_WITH: "XMLHttpRequest",
      "X-Requested-With": "XMLHttpRequest",
    },
    credentials: "include",
    body: data,
  };
  fetch("/auth/login/", requestOptions)
    .then((response) => response.json())
    .then((data) => {
      if (data["success"] === "true") {
        localStorage.setItem("username", data["username"]);
        successCallback();
      } else if (data["success"] === "false") {
        updateErrorsCallback([data["message"]]);
      }
    })
    .catch((error) => console.error(error));
};

const handleRegistrationSubmission = async (
  e,
  updateErrorsCallback,
  successCallback
) => {
  updateErrorsCallback([]);
  e.preventDefault();
  if (
    e.target[0].value.trim() === "" ||
    e.target[1].value.trim() === "" ||
    e.target[2].value.trim() === "" ||
    e.target[3].value.trim() === ""
  ) {
    return;
  }

  let data = new FormData(e.target);

  const requestOptions = {
    method: "POST",
    headers: {
      "X-CSRFToken": await getCsrfToken(),
      Accept: "application/json",
      HTTP_X_REQUESTED_WITH: "XMLHttpRequest",
      "X-Requested-With": "XMLHttpRequest",
    },
    credentials: "include",
    body: data,
  };
  fetch("/auth/register/", requestOptions)
    .then((response) => response.json())
    .then((data) => {
      if (data["success"] === "unknown") {
        // localStorage.setItem("username", data["username"]);
        successCallback([data["message"]]);
      } else if (data["success"] === "false") {
        // console.log(data["errors"]);
        updateErrorsCallback(data["errors"]);
      }
    })
    .catch((error) => console.log(error));
};

const handleLogoutSubmission = async () => {
  const [authenticated, username] = await isAuthenticatedStrict();
  if (authenticated === true) {
    fetch("/auth/logout/", {
      method: "POST",
      headers: {
        "X-CSRFToken": await getCsrfToken(),
        Accept: "application/json",
        HTTP_X_REQUESTED_WITH: "XMLHttpRequest",
        "X-Requested-With": "XMLHttpRequest",
      },
    });
  }
  localStorage.removeItem("username");
  return true;
};

export {
  handleRegistrationSubmission,
  handleLoginSubmission,
  handleLogoutSubmission,
};
