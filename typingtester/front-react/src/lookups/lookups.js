const isAuthenticatedStrict = async () => {
  return await fetch("/auth/v2/user/", {
    method: "GET",
    headers: {
      Accept: "application/json",
    },
  })
    .then((_res) => {
      return _res.json();
    })
    .then((data) => {
      if ('pk' in data) {
        return [true, data['username']];
      }
      return [false, null];
    })
    .catch((err) => {
      alert(err);
    });
};

const isAuthenticated = async () => {
    return isAuthenticatedStrict();
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
  isAuthenticated,
  isAuthenticatedStrict,
  getQuote,
  loadStatistics,
  loadTestRecords,
  fetchUserInfo,
};
