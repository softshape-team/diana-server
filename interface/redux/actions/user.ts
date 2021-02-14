import axios from "axios";
import { request } from "http";
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

const authenticateByTokens = () => async (dispatch: Function) => {
  const requestUser = async () => {
    const accessToken = localStorage.getItem("accessToken");
    const refreshToken = localStorage.getItem("refreshToken");

    try {
      const res = await axios.get(`${base}/accounts/user/`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });

      const user = res.data.user;

      dispatch(loginSucceed(accessToken, refreshToken, user));

      return true;
    } catch (err) {
      return false;
    }
  };

  const refreshTokenRequest = async () => {
    let accessToken = localStorage.getItem("accessToken");
    let refreshToken = localStorage.getItem("refreshToken");

    try {
      const res = await axios.post(`${base}/accounts/token/refresh/`, {
        refresh: refreshToken,
      });

      accessToken = res.data.access;
      refreshToken = res.data.refresh;
      localStorage.setItem("accessToken", accessToken);
      localStorage.setItem("refreshToken", refreshToken);

      return true;
    } catch (err) {
      return false;
    }
  };

  let res = await requestUser();

  // TODO: review need to be simplified
  if (res) {
    return true;
  } else {
    res = await refreshTokenRequest();

    if (res) {
      res = await requestUser();
      return res;
    } else {
      return false;
    }
  }
};

export default types;
export {
  loginRequested,
  loginSucceed,
  loginFailed,
  loginRequest,
  authenticateByTokens,
};
