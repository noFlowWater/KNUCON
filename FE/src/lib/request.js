import qs from "qs"

const request = async (operation, url, params, headers) => {
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

  const response = await fetch(_url, options);
    if (response.status === 204 || response.status === 205) {
        // No content or Reset content, no need to parse JSON
        console.log('Response status:', response.status, 'No content or Reset content');
        return null;
    } else if (response.status >= 200 && response.status < 300) {
        console.log('Response status:', response.status, 'Success');

        // 응답 내용을 JSON으로 파싱하기 전에 응답의 일부 정보를 로깅
        console.log('Response headers:', response.headers);
        console.log('Response URL:', response.url);
        console.log('Response type:', response.type);

        const responseData = await response.json();

        // 응답 데이터 로깅
        console.log('Response data:', responseData);
        return responseData;
    } else {
        console.log('Response status:', response.status, 'Error');
        const errorData = await response.json();
        console.log('Error data:', errorData);
        throw new Error(JSON.stringify(errorData));
    }

};

export default request;
