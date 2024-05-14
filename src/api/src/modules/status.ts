import { API, APIDEFAULT } from "../dictionaries/API";
import cache from "./cache";
import config from "../config.json";

class Status {
  public API: Promise<any> | null = null;
  public data: Promise<API | APIDEFAULT> | null = null;
  private API_URL: string = `https://api.steampowered.com/ICSGOServers_730/GetGameServersStatus/v1/?key=${config.KEY}`;
  private default_json = {
    result: {
      services: "unknown",
      datacenters: "unknown",
      matchmaking: "unknown",
    },
  };

  private async setAPI(): Promise<void> {
    const getCache = cache.get("status") as Promise<any>;

    if (!(await getCache)) {
      const response = await fetch(this.API_URL, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });
      const data = await response.json();
      cache.put("status", data, 35);

      this.API = Promise.resolve(data);
      return;
    }

    this.API = Promise.resolve(getCache);
  }

  public async getStatus(): Promise<API | APIDEFAULT> {
    await this.setAPI();
    if (!this.API) return this.default_json as APIDEFAULT;

    this.data = this.API.then((data) => {
      if (data == null) return this.default_json as APIDEFAULT;
      return data as unknown as Promise<API>;
    });

    const data = await this.data;
    if (!data) return this.default_json as APIDEFAULT;

    return {
      result: {
        services: data.result.services,
        datacenters: data.result.datacenters,
        matchmaking: data.result.matchmaking,
      },
    };
  }
}

export default new Status();
