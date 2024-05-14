import GlobalOffensive from "globaloffensive";
import SteamClient from "./steam";

//
// Counter-Strike Client
// This class runs a headless Counter-Strike Client.
//

class CounterStrikeClient extends GlobalOffensive {
  constructor() {
    super(SteamClient);
    console.log("Counter-Strike client online.");
  }
}

export default new CounterStrikeClient();
