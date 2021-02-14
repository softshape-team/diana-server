import { createStore, applyMiddleware } from "redux";
import { MakeStore, createWrapper, Context } from "next-redux-wrapper";
import { composeWithDevTools } from "redux-devtools-extension/developmentOnly";
import thunk from "redux-thunk";
import reducer from "./reducers";

const middlewares = [thunk];

if (process.env.NODE_ENV === "development") {
  const { logger } = require("redux-logger");
  middlewares.push(logger);
}

const makeStore: MakeStore = (context: Context) => {
  return createStore(
    reducer,
    composeWithDevTools(applyMiddleware(...middlewares))
  );
};

const wrapper = createWrapper(makeStore, { debug: true });

export default wrapper;
