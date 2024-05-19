import SteamUser from "steam-user";
import SteamClient from "./clients/steam";
import cache from "./cache";
import type {
  ProductChanges,
  PackageChanges,
  AppChanges,
} from "../dictionaries/Steam";

class SteamAppChanges {
  private Steam: SteamUser;

  constructor() {
    this.Steam = SteamClient;
  }

  /**
   *
   * @param change_number the ID of the Steam application
   * @returns Promise
   */

  async ProductChanges(change_number: number): Promise<ProductChanges> {
    const app = cache.get(change_number.toString()) as ProductChanges;
    if (!app) {
      const app = await this.Steam.getProductChanges(
        change_number,
        (err, change) => {
          if (err) throw err;

          return this.Steam.picsCache.apps[change];
        }
      );
      cache.put(change_number.toString(), cache, 3);
      return app;
    }
    return app;
  }

  /**
   *
   * @param change_number the ID of the Steam application
   * @returns Promise
   */

  async PackageChanges(change_number: number): Promise<PackageChanges> {
    const app = await this.ProductChanges(change_number);
    return app.packageChanges;
  }

  /**
   *
   * @param change_number the ID of the Steam application
   * @returns Promise
   */

  async AppChanges(change_number: number): Promise<AppChanges> {
    const app = await this.ProductChanges(change_number);
    return app.appChanges;
  }

  /**
   *
   * @param appid the ID of the Steam application
   * @returns Promise
   */

  async AppUpdate(appid?: number): Promise<string | Record<string, unknown>> {
    if (appid) return this.Steam.picsCache.apps[appid];
    return this.Steam.picsCache.apps;
  }
}

export default new SteamAppChanges();
