import SteamUser from "steam-user";
import SteamClient from "./clients/steam";
import type { ProductInfo } from "../dictionaries/Steam";
import cache from "./cache";

class SteamAppInformation {
  private Steam: SteamUser;

  constructor() {
    this.Steam = SteamClient;
  }

  /**
   *
   * @param appid the ID of the Steam application
   * @returns Null or the Steam application's information
   */

  async ProductInfo(appid: number): Promise<ProductInfo | {}> {
    const data = cache.get(appid.toString());

    if (!data) {
      const data = await this.Steam.getProductInfo(
        [appid],
        [],
        true,
        (_, apps, packages, unknownApps, unknownPackages) => [
          apps,
          packages,
          unknownApps,
          unknownPackages,
        ]
      );

      cache.put(appid.toString(), data, 45);

      return data;
    }
    return data;
  }
}

export default new SteamAppInformation();
