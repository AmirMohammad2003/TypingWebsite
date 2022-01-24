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

const isAuthenticatedStrict = () => {
  let username = fetch("/auth/check")
    .then((_res) => _res.json())
    .then((data) => {
      if (data["success"] === "true") {
        localStorage.setItem("username", username);
        return [true, username];
      } else {
        return [false, null];
      }
    })
    .catch((err) => {
      alert(err);
    });
};

const isAuthenticated = () => {
  let username = localStorage.getItem("username");
  if (!username) {
    let [authenticated, username] = isAuthenticatedStrict();
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
    csrftoken = await fetch("/api/csrf", {
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
    xhr.open("GET", "/api/load");
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xhr.setRequestHeader("HTTP_X_REQUESTED_WITH", "XMLHttpRequest");
    // xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.send();
  });
};

export { getCookie, getCsrfToken, isAuthenticated, isAuthenticatedStrict };
export default getQuote;
