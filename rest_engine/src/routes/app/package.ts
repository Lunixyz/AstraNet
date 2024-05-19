import router from "../router";
import app_changes from "../../modules/app_changes";

//
// Package update query route
// This route basically displays every package that was updated
// in the specified changenumber. Useful for queries!
//

export default () =>
  router.get("/app/package/:id", async (req, res) => {
    const id = req.params.id;
    return res.status(200).json({
      data: await app_changes.PackageChanges(parseInt(id)),
    });
  });
