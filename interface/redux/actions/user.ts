import baseAxios from "axios";
import { UserActionTypes, Action, Credentials } from "../../tstypes";

const axios = baseAxios.create({
  baseURL: "http://localhost:8000",
});

const types: UserActionTypes = {
  // Login
  LOGIN_REQUESTED: "Login request has been sent.",
  LOGIN_SUCCEED: "Login request has been succeed.",
  LOGIN_FAILED: "Login request has been failed.",

  // Logout
  LOGOUT_REQUESTED: "Logout request has been sent.",
  LOGOUT_SUCCEED: "Logout request has been succeed.",
  LOGOUT_FAILED: "Logout request has been failed.",
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

const logoutRequested = () => ({
  type: types.LOGOUT_REQUESTED,
});

const logoutSucceed = () => ({
  type: types.LOGOUT_SUCCEED,
});

const logoutFailed = (errs: object) => ({
  type: types.LOGOUT_FAILED,
  payload: {
    errs: errs,
  },
});

const loginRequest = (cred: Credentials) => async (dispatch: Function) => {
  dispatch(loginRequested());

  try {
    const res = await axios.post("/accounts/login/", {
      username: cred.username,
      password: cred.password,
    });

    const accessToken = res.data.access_token;
    const refreshToken = res.data.refresh_token;
    const user = res.data.user;

    dispatch(loginSucceed(accessToken, refreshToken, user));
    return true;
  } catch (errs) {
    dispatch(loginFailed(errs.response.data));
    return false;
  }
};

const authenticateByTokens = () => async (dispatch: Function) => {
  const requestUser = async () => {
    const accessToken = localStorage.getItem("accessToken");
    const refreshToken = localStorage.getItem("refreshToken");

    if (!accessToken || !refreshToken) {
      return false;
    }

    try {
      const res = await axios.get("/accounts/user/", {
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

    if (!accessToken || !refreshToken) {
      return false;
    }

    try {
      const res = await axios.post("/accounts/token/refresh/", {
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

const logoutRequest = (accessToken: string) => async (dispatch: Function) => {
  dispatch(logoutRequested());
  try {
    const res = await axios.post("/accounts/logout/", {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });
    dispatch(logoutSucceed());
    return true;
  } catch (errs) {
    dispatch(logoutFailed(errs.response.data));
    return false;
  }
};

export default types;
export {
  // Login
  loginRequested,
  loginSucceed,
  loginFailed,
  loginRequest,
  authenticateByTokens,
  // Logout
  logoutRequested,
  logoutSucceed,
  logoutFailed,
  logoutRequest,
};
