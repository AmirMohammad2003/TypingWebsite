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
        sessionStorage.setItem("username", data["username"]);
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
        successCallback([data["message"]]);
      } else if (data["success"] === "false") {
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
  sessionStorage.removeItem("username");
  return true;
};

const handleResetPassword = async (
  email,
  updateErrorsCallback,
  successCallback
) => {
  updateErrorsCallback([]);
  if (email === "") {
    return;
  }
  let data = new FormData();
  data.append("email", email);

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
  fetch("/auth/reset/", requestOptions)
    .then((response) => response.json())
    .then((data) => {
      if (data["success"] === "true") {
        successCallback([data["message"]]);
      } else if (data["success"] === "false") {
        updateErrorsCallback(data["errors"]);
      }
    })
    .catch((error) => console.log(error));
};

const handleResetPasswordConfirmation = async (
  e,
  uidb64,
  token,
  errorsCallback,
  successCallback
) => {
  if (e.target[0].value.trim() === "" || e.target[1].value.trim() === "") {
    return;
  }

  if (e.target[0].value.trim() !== e.target[1].value.trim()) {
    errorsCallback(["Passwords Should match."]);
    return;
  }
  errorsCallback([]);

  let data = new FormData(e.target);
  data.append("uidb64", uidb64);
  data.append("token", token);

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
  fetch("/auth/reset/confirm/", requestOptions)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      if (data["success"] === "true") {
        successCallback([data["location"]]);
      } else if (data["success"] === "false") {
        errorsCallback(data["errors"]);
      }
    })
    .catch((error) => console.log(error));
};

const handleChangePassword = async (
  e,
  errorsCallback,
  successCallback,
  location
) => {
  if (
    e.target[0].value.trim() === "" ||
    e.target[1].value.trim() === "" ||
    e.target[2].value.trim() === ""
  ) {
    return;
  }

  if (e.target[1].value.trim() !== e.target[2].value.trim()) {
    errorsCallback(["Passwords Should match."]);
    return;
  }
  errorsCallback([]);

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
  fetch("/auth/password/change/", requestOptions)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      if (data["success"] === "true") {
        successCallback(location);
      } else if (data["success"] === "false") {
        errorsCallback(data["errors"]);
      }
    })
    .catch((error) => console.log(error));
};

const handleResendRequestForPasswordReset = async () => {
  fetch("/auth/resend/verification/", {
    method: "POST",
    headers: {
      "X-CSRFToken": await getCsrfToken(),
      Accept: "application/json",
      HTTP_X_REQUESTED_WITH: "XMLHttpRequest",
      "X-Requested-With": "XMLHttpRequest",
    },
    credentials: "include",
  });
  return true;
};

export {
  handleRegistrationSubmission,
  handleLoginSubmission,
  handleLogoutSubmission,
  handleResetPassword,
  handleResetPasswordConfirmation,
  handleChangePassword,
  handleResendRequestForPasswordReset,
};
