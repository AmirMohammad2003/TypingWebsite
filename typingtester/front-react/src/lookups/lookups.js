function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const isAuthenticatedStrict = async () => {
  let [authenticated, username] = await fetch("/auth/check/", {
    method: "POST",
    headers: {
      Accept: "application/json",
      "X-CSRFToken": await getCsrfToken(),
    },
  })
    .then((_res) => {
      return _res.json();
    })
    .then((data) => {
      if (data["Authenticated"] === "true") {
        sessionStorage.setItem("username", data["username"]);
        return [true, data["username"]];
      } else {
        return [false, null];
      }
    })
    .catch((err) => {
      alert(err);
    });

  if (authenticated) return [authenticated, username];

  return [false, null];
};

const isAuthenticated = async () => {
  let username = sessionStorage.getItem("username");
  if (!username) {
    let [authenticated, username] = await isAuthenticatedStrict();
    if (authenticated === true) {
      return [true, username];
    } else {
      return [false, null];
    }
  } else {
    return [true, username];
  }
};

const getCsrfToken = async () => {
  // if the frontend is generated as a template by the django frontend application
  // csrf token is already present in the cookie
  let csrftoken = getCookie("csrftoken");
  if (csrftoken !== null && csrftoken !== undefined) {
    return csrftoken;
  } else {
    // if the frontend is living on a different server so it's not in the cookie
    // we need to retrieve the csrf token from the server
    csrftoken = await fetch("/api/csrf/", {
      method: "GET",
    })
      .then((_res) => {
        if (_res.statusCode === 200) {
          return _res.json();
        }
        return { token: null };
      })
      .then((data) => data.token)
      .catch((error) => alert(error));
  }

  return csrftoken;
};

const getQuote = () => {
  return new Promise((resolve) => {
    console.log("i ran");
    const xhr = new XMLHttpRequest();
    xhr.responseType = "text";
    xhr.onload = () => {
      if (xhr.status === 200) {
        resolve(xhr.response);
      }
    };
    xhr.onerror = () => {
      alert("Error");
    };
    xhr.open("GET", "/api/load/");
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xhr.setRequestHeader("HTTP_X_REQUESTED_WITH", "XMLHttpRequest");
    xhr.send();
  });
};

const loadStatistics = async () => {
  const requestOptions = {
    method: "POST",
    headers: {
      "X-CSRFtoken": await getCsrfToken(),
      Accept: "application/json",
    },
  };

  return fetch("/api/load-statistics/", requestOptions)
    .then((response) => {
      if (response.status === 200) {
        return response.json();
      } else {
        return null;
      }
    })
    .then((data) => data)
    .catch((error) => console.log(error));
};

const loadTestRecords = async () => {
  const requestOptions = {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
  };

  return fetch("/api/load-test-records/", requestOptions)
    .then((response) => {
      if (response.status === 200) {
        return response.json();
      } else {
        return null;
      }
    })
    .then((data) => data)
    .catch((error) => console.log(error));
};

const fetchUserInfo = async () => {
  const requestOptions = {
    method: "POST",
    headers: {
      "X-CSRFtoken": await getCsrfToken(),
      Accept: "application/json",
    },
  };

  return fetch("/auth/user/info/", requestOptions)
    .then((response) => {
      if (response.status === 200) {
        return response.json();
      } else {
        return null;
      }
    })
    .then((data) => data)
    .catch((error) => console.log(error));
};

export {
  getCookie,
  getCsrfToken,
  isAuthenticated,
  isAuthenticatedStrict,
  getQuote,
  loadStatistics,
  loadTestRecords,
  fetchUserInfo,
};
