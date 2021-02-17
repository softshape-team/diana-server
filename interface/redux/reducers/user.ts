import { Action } from "../../tstypes";
import { user as types } from "../actions/types";

const init = {
  isAuthed: false,
  isLoading: false,
  accessToken: null,
  refreshToken: null,
  user: null,
  errs: null,
};

const reducer = (state = init, action: Action) => {
  switch (action.type) {
    default:
      return state;

    case types.LOGIN_REQUESTED:
      return {
        ...init,
        isLoading: true,
      };

    case types.LOGIN_SUCCEED:
      const accessToken = action.payload.accessToken;
      const refreshToken = action.payload.refreshToken;
      localStorage.setItem("accessToken", accessToken);
      localStorage.setItem("refreshToken", refreshToken);

      return {
        ...init,
        isAuthed: true,
        isLoading: false,
        accessToken: action.payload.accessToken,
        refreshToken: action.payload.refreshToken,
        user: action.payload.user,
      };

    case types.LOGIN_FAILED:
      return {
        ...init,
        isAuthed: false,
        isLoading: false,
        accessToken: null,
        refreshToken: null,
        user: null,
        errs: action.payload.errs,
      };

    case types.LOGOUT_REQUESTED:
      return {
        ...state,
        isLoading: true,
      };

    case types.LOGOUT_SUCCEED:
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
      return {
        ...state,
        isAuthed: null,
        accessToken: null,
        refreshToken: null,
        user: null,
        errs: null,
      };

    case types.LOGOUT_FAILED:
      return {
        ...state,
        errs: action.payload.errs,
      };
  }
};

export default reducer;
