export type ActionType = string;

export interface ActionTypes {
  [key: string]: string;
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
