import router from "../router";
import status from "../../modules/status";

//
// Status route.
// This route displays the current server statuses of Counter-Strike's
// datacenters. Very useful for automations.
//

export default () =>
  router.get("/app/730/status", async (_, res) => {
    return res.status(200).json({
      data: await status.getStatus(),
    });
  });
