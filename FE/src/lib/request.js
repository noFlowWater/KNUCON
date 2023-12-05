import qs from "qs"

const request = async (operation, url, params, headers = {}) => {
  let method = operation.toUpperCase();
  let _url = 'http://192.168.0.165:8000' + url;

  // 기본 헤더 설정
  const defaultHeaders = {
    "Content-Type": 'application/json',
    ...headers
  };
  
  if (method === 'GET') {
    _url += new URLSearchParams(params).toString();
  }

  let options = {
    method: method,
    headers: defaultHeaders,
    credentials: 'include',
  };
  
  if (method !== 'GET') {
    options['body'] = JSON.stringify(params);
  }

  if (operation === 'login') {
    console.log('login!!!!')
    options.method = 'POST';
    options.headers["Content-Type"] = 'application/x-www-form-urlencoded';
    options.body = qs.stringify(params);
  }

  const response = await fetch(_url, options);
  console.log('---- < response > ----')
  if (response.status === 204 || response.status === 205) {
      // No content or Reset content, no need to parse JSON
      console.log(`Response status: ${response.status}, No content or Reset content`);
      console.log('----------------------')
      return null;
  } else if (response.status >= 200 && response.status < 300) {
      console.log('Response status:', response.status, 'Success');

      // Fetching response data
      const responseData = await response.json();

      // Consolidated logging
      console.log(`Response details:
          Status: ${response.status}
          Headers: ${JSON.stringify([...response.headers])}
          URL: ${response.url}
          Type: ${response.type}
          Data: ${JSON.stringify(responseData)}
      `);
      console.log('----------------------')
      return responseData;
  } else {
      console.log('Response status:', response.status, 'Error');
      const errorData = await response.json();
      console.log('Error data:', errorData);
      throw new Error(JSON.stringify(errorData));
  }
};

export default request;
