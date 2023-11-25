import qs from "qs"

const request = async (operation, url, params, headers, username, password, credentials = 'include') => {
  let method = operation.toUpperCase();
  let _url = 'http://localhost:8000' + url;

  if (method === 'GET') {
    _url += new URLSearchParams(params).toString();
  }

  let options = {
    method: method,
    headers: {
      "Content-Type": 'application/json',
      ...headers
    },
    credentials: 'include',
  };

  if (method !== 'GET') {
    options['body'] = JSON.stringify(params);
  }

  if (operation === 'login') {
    options.method = 'POST';
    options.headers["Content-Type"] = 'application/x-www-form-urlencoded';
    options.body = qs.stringify(params);
  }

  fetch(_url, options)
        .then(response => {
            response.json()
                .then(json => {
                    if(response.status >= 200 && response.status < 300) {  // 200 ~ 299
                        if(success_callback) {
                            success_callback(json)
                        }
                    }else {
                        if (failure_callback) {
                            failure_callback(json)
                        }else {
                            alert(JSON.stringify(json))
                        }
                    }
                })
                .catch(error => {
                    alert(JSON.stringify(error))
                })
        })
};

export default request;
