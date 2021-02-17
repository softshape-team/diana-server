import { Action } from "../../tstypes";
import { registration as types } from "../actions/types";

const init = {
  isLoading: false,
  user: null,
  errs: null,
};

const reducer = (state = init, action: Action) => {
  switch (action.type) {
    default:
      return state;

    case types.REGISTRATION_REQUESTED:
      return {
        ...state,
        isLoading: true,
      };

    case types.REGISTRATION_SUCCEED:
      return {
        ...state,
        isLoading: false,
        user: action.payload.user,
        errs: null,
      };

    case types.REGISTRATION_FAILED:
      return {
        ...state,
        isLoading: false,
        user: null,
        errs: action.payload.errs,
      };
  }
};

export default reducer;
