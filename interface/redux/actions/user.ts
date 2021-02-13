import axios from "axios";
import { ActionTypes, Action, Credentials } from "../../tstypes";

const base = "http://localhost:8000";

const types: ActionTypes = {
  LOGIN_REQUESTED: "Login request has been sent.",
  LOGIN_SUCCEED: "Login request has been succeed.",
  LOGIN_FAILED: "Login request has been failed.",
};

const loginRequested = (): Action => ({
  type: types.LOGIN_REQUESTED,
});

const loginSucceed = (
  accessToken: string,
  refreshToken: string,
  user: object
): Action => ({
  type: types.LOGIN_SUCCEED,
  payload: {
    accessToken,
    refreshToken,
    user,
  },
});

const loginFailed = (errs: object): Action => ({
  type: types.LOGIN_FAILED,
  payload: {
    errs,
  },
});

const loginRequest = (cred: Credentials) => async (dispatch: Function) => {
  dispatch(loginRequested());

  try {
    const res = await axios.post(`${base}/accounts/login/`, {
      username: cred.username,
      password: cred.password,
    });

    const accessToken = res.data.access_token;
    const refreshToken = res.data.refresh_token;
    const user = res.data.user;

    dispatch(loginSucceed(accessToken, refreshToken, user));
    return true;
  } catch (err) {
    dispatch(loginFailed(err.response.data));
    return false;
  }
};

export default types;
export { loginRequested, loginSucceed, loginFailed, loginRequest };
