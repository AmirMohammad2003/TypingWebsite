import { isAuthenticatedStrict } from "./lookups";

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
      Accept: "application/json",
      HTTP_X_REQUESTED_WITH: "XMLHttpRequest",
      "X-Requested-With": "XMLHttpRequest",
    },
    credentials: "include",
    body: data,
  };
  fetch("/auth/v2/login/", requestOptions)
    .then((response) => response.json())
    .then((data) => {
      if ('access_token' in data) {
        console.log(data)
        successCallback(data['user']['username']);
      } else  {
        if ('non_field_errors' in data) {
          updateErrorsCallback([data["non_field_errors"]]);
        } else {
          updateErrorsCallback(["Something went wrong please try again later."]);
        }
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
      Accept: "application/json",
      HTTP_X_REQUESTED_WITH: "XMLHttpRequest",
      "X-Requested-With": "XMLHttpRequest",
    },
    credentials: "include",
    body: data,
  };
  fetch("/auth/v2/registration/", requestOptions)
    .then((response) => response.json())
    .then((data) => {
      if ("user" in data) {
        successCallback(data['user']);
      } else {
        updateErrorsCallback(data);
      }
    })
    .catch((error) => console.log(error));
};

const handleLogoutSubmission = async () => {
  fetch("/auth/v2/logout/", {
    method: "POST",
    headers: {
      Accept: "application/json",
      HTTP_X_REQUESTED_WITH: "XMLHttpRequest",
      "X-Requested-With": "XMLHttpRequest",
    },
  });
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
      Accept: "application/json",
      HTTP_X_REQUESTED_WITH: "XMLHttpRequest",
      "X-Requested-With": "XMLHttpRequest",
    },
    credentials: "include",
    body: data,
  };
  fetch("/auth/v2/reset/", requestOptions)
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
      Accept: "application/json",
      HTTP_X_REQUESTED_WITH: "XMLHttpRequest",
      "X-Requested-With": "XMLHttpRequest",
    },
    credentials: "include",
    body: data,
  };
  fetch("/auth/v2/reset/confirm/", requestOptions)
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
      Accept: "application/json",
      HTTP_X_REQUESTED_WITH: "XMLHttpRequest",
      "X-Requested-With": "XMLHttpRequest",
    },
    credentials: "include",
    body: data,
  };
  fetch("/auth/v2/password/change/", requestOptions)
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
  fetch("/auth/v2/resend/verification/", {
    method: "POST",
    headers: {
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
