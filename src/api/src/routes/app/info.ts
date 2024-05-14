import router from "../router";
import app_info from "../../modules/app_info";

//
// Application information route.
// This route displays information about a Steam App.
// All information listed on this route is the same as
// what is displayed on the Steam Store.
//

export default () =>
  router.get("/app/:appid/info", async (req, res) => {
    const appid = req.params.appid;

    return res.status(200).json({
      data: await app_info.ProductInfo(parseInt(appid)),
    });
  });
