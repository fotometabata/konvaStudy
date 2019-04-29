import { Promise } from 'es6-promise';
import ajax from '../api/Ajax/commonAjax';
import State from './index';
import { isCookieEnabled, setCookie, getCookie } from 'tiny-cookie';

const baseApiUrl = 'api/1.0/';
export default {
  SAVE_IMAGE_FILE: ({commit}, payload) => {
    return new Promise((resolve, reject) => {
      ajax.postRequest(baseApiUrl + 'saveImageFile/', payload,
      function(res) {
        resolve(res);
      }, function(error) {
        reject(error);
      });
    });
  },
  SET_TOKEN: ({commit}, payload) => {
    return new Promise((resolve, reject) => {
      ajax.postRequest(baseApiUrl + 'token/', payload,
        function(res) {
          commit('SET_TOKEN', res.data);
          if (isCookieEnabled()) {
            setCookie('id_token', res.data.token);
            resolve(res)
          } else {
            reject();
          }
        }, function(error) {
          reject(error)
        }
      );
    })
  },
  CHECK_TOKEN: ({commit}, payload) => {
    return new Promise((resolve, reject) => {
      let token = '';
      let cookieEnabled = isCookieEnabled();
      if (cookieEnabled) {
        token = getCookie('id_token');
      }
      if (token && cookieEnabled) {
        State.state.authenticate = true;
        resolve();
      } else {
        State.state.authenticate = false;
        reject();
      }
    })
  }
}