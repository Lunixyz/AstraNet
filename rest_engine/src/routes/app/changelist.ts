import router from "../router";
import appChanges from "../../modules/app_changes";

//
// Steam's PIC route
// This route displays the current PIC list,
// useful for keeping track of app updates!
//

export default () =>
  router.get("/app/:appid?/changelist", async (req, res) => {
    const appid = req.params.appid;

    return res.status(200).json({
      appid: appid ? parseInt(appid) : "unknown",
      data: await appChanges.AppUpdate(appid ? parseInt(appid) : undefined),
    });
  });
