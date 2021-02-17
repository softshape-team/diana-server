export type ActionType = string;

export interface ActionTypes {
  [key: string]: string;
}

export interface RegistrationActionTypes {
  REGISTRATION_REQUESTED: string;
  REGISTRATION_SUCCEED: string;
  REGISTRATION_FAILED: string;
}

export interface UserActionTypes {
  LOGIN_REQUESTED: string;
  LOGIN_SUCCEED: string;
  LOGIN_FAILED: string;
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

export interface user {
  firstName: string;
  lastName: string;
  username: string;
  email: string;
  password: string;
}
