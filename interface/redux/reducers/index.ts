import { combineReducers } from "redux";
import user from "./user";
import registration from "./registration";

const reducers = combineReducers({
  user,
  registration,
});

export default reducers;
