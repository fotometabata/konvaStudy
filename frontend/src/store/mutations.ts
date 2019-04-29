export default {
  SET_TOKEN: (state, payload) => {
    state.token = payload.token;
    state.authenticate = false;
  }
}