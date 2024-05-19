import { Router } from "express";
import { readdirSync } from "fs";

export default Router();

class Routes {
  async loadAppRoutes(): Promise<void> {
    const approutes = readdirSync(`${process.cwd()}/rest_engine/dist/src/routes/app`);
    for (const files of approutes) {
      if (files.endsWith(".js")) {
        const module = await import(
          `${process.cwd()}/rest_engine/dist/src/routes/app/${files}`
        );

        module.default();
      }
    }
  }
}

export { Routes };
