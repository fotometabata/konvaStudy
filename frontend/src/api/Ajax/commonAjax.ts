import axios from 'axios';
import { getCookie, isCookieEnabled, removeCookie } from 'tiny-cookie';

// Djangoサーバーへのリクエスト用URLのベース
let SERVER_BASE_URL = location.origin;
if (location.port) {
    SERVER_BASE_URL = SERVER_BASE_URL.replace('localhost', '127.0.0.1');
    SERVER_BASE_URL = SERVER_BASE_URL.replace(location.port, '8000');
}
SERVER_BASE_URL = SERVER_BASE_URL + '/';

/**
 * Post通信（Ajax）
 * @param url URL
 * @param data データ
 * @param resolve 成功時
 * @param reject 失敗時
 */
const postRequest = function(url, data, resolve, reject) {
  const requestUrl = SERVER_BASE_URL + url;
  const header = {
    headers: {
      'Content-Type': 'application/json'
    }
  };

  var token = isCookieEnabled() ? getCookie('id_token') : '';
  if (!!token) {
    header.headers['Authorization'] = `JWT ${token}`;
  }

  const http = axios.create(header);
  http.post(requestUrl, data).then(res => {
    resolve(res)
  }).catch(error => {
    console.log(error);
    if (error.response && error.response.status) {
      checkAuthorization(error.response.status);
    }
    reject(error)
  });
}

/**
 * 
 * @param errorStatusCode
 */
function checkAuthorization(errorStatusCode) {
  if (errorStatusCode === 401) {
    removeCookie('id_token');
    if (!/login/.test(location.href)) {
      console.log('ログイン画面へ');
      location.href = '/login';
    }
  }
}

export default {
  postRequest
}
