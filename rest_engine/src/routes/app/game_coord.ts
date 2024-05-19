import router from "../router";
import gc from "../../modules/game_coordinator";

//
// Status route.
// This route displays the current server statuses of Counter-Strike's
// datacenters. Very useful for automations.
//

export default () =>
  router.get("/app/730/gc", async (_, res) => {
    return res.status(200).json({
      data: gc.getStatus(),
    });
  });
