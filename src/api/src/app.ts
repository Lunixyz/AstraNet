import express from "express";
import csurf from "csurf";
import helmet from "helmet";
import cookieParser from "cookie-parser";
import bodyParser from "body-parser";
import * as dotenv from "dotenv";
import router, { Routes } from "./routes/router";

const app = express();

dotenv.config();

app.use(cookieParser());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(csurf({ cookie: { httpOnly: true, secure: true } }));

app.use((err, res, next) => {
  if (err && err.statusMessage === "EBADCSRFTOKEN") {
    res.status(403).send("CSRF Token is invalid!");
  } else {
    next();
  }
});
app.use(helmet());
app.use(router);
app.set("json spaces", 2);

(async () => {
  const routes = new Routes();
  await routes.loadAppRoutes();
})();

export { app };
