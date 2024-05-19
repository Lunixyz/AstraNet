import cs from "./clients/cs";
import {
  TrueGCConnectionStatus,
  GC,
  GCConnectionStatus,
} from "../dictionaries/API";

class GameCoordinatorStatus {
  getStatus(): GC {
    let gc: GC | null = null;

    if (!cs.haveGCSession)
      return {
        result: {
          game_coordinator: "not_connected",
        },
      };

    cs.on("connectedToGC", () => {
      console.log("hi GC omg");
      gc = {
        result: {
          game_coordinator:
            TrueGCConnectionStatus[GCConnectionStatus.HAVE_SESSION],
        },
      };
    });

    cs.on("disconnectedFromGC", (r) => {
      console.log("oh noes bye gc");
      gc = {
        result: {
          game_coordinator: TrueGCConnectionStatus[r],
        },
      };
    });

    if (!gc)
      return {
        result: {
          game_coordinator: "unknown",
        },
      };

    return gc;
  }
}

export default new GameCoordinatorStatus();
