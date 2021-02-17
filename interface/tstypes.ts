export type ActionType = string;

export interface ActionTypes {
  [key: string]: string;
}

export interface RegistrationActionTypes {
  REGISTRATION_REQUESTED: string;
  REGISTRATION_SUCCEED: string;
  REGISTRATION_FAILED: string;
}

export interface Payload {
  [key: string]: any;
}

export interface Action {
  type: ActionType;
  payload?: Payload;
}

export interface Credentials {
  username: string;
  password: string;
}

export interface userObject {
  firstName: string;
  lastName: string;
  username: string;
  email: string;
  password: string;
}
