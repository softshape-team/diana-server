import { createStore, applyMiddleware } from "redux";
import { MakeStore, createWrapper, Context } from "next-redux-wrapper";
import thunk from "redux-thunk";
import logger from "redux-logger";
import reducer from "./reducers";

// TODO: apply logger middleware only on development environment
const makeStore: MakeStore = (context: Context) => {
  return createStore(reducer, applyMiddleware(thunk, logger));
};

const wrapper = createWrapper(makeStore, { debug: true });

export default wrapper;
