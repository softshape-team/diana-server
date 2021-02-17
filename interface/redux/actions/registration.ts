import baseAxios from "axios";
import { RegistrationActionTypes, Action, userObject } from "../../tstypes";

const axios = baseAxios.create({
  baseURL: "http://localhost:8000",
});

const types: RegistrationActionTypes = {
  REGISTRATION_REQUESTED: "Registration request has been sent.",
  REGISTRATION_SUCCEED: "Registration has been succeed",
  REGISTRATION_FAILED: "Registration has been failed",
};

const registrationRequested = (): Action => ({
  type: types.REGISTRATION_REQUESTED,
});

const registrationSucceed = (user: object): Action => ({
  type: types.REGISTRATION_SUCCEED,
  payload: {
    user,
  },
});

const registrationField = (err: any): Action => ({
  type: types.REGISTRATION_FAILED,
  payload: {
    err,
  },
});

const registrationRequest = (userData: userObject) => async (
  dispatch: Function
) => {
  dispatch(registrationRequested());

  try {
    const user = await axios.post("/accounts/registration/", {
      first_name: userData.firstName,
      last_name: userData.lastName,
      username: userData.username,
      email: userData.email,
      password: userData.password,
    });

    dispatch(registrationSucceed(user));
    return true;
  } catch (errs) {
    dispatch(registrationField(errs));
    return false;
  }
};

export default types;
export {
  registrationRequested,
  registrationSucceed,
  registrationField,
  registrationRequest,
};
