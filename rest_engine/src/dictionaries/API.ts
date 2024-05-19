export enum STATUS {
  offline = "offline",
  surge = "crítico",
  delayed = "lento",
  normal = "normal",
}

export enum LOAD {
  idle = "inativo",
  low = "baixo",
  medium = "médio",
  high = "alto",
}

export enum CAPACITY {
  low = "baixa",
  medium = "média",
  high = "alta",
  full = "cheio",
}

export interface MATCHMAKING {
  scheduler: STATUS;
  online_servers: number;
  online_players: number;
  searching_players: number;
  search_seconds_avg: number;
}

export interface SERVICES {
  SessionsLogon: STATUS;
  SteamCommunity: STATUS;
  IEconItems: STATUS;
  Leaderboards: STATUS;
}

export interface DATACENTERINF {
  capacity: CAPACITY;
  load: LOAD;
}

export interface DATACENTERS {
  Peru: DATACENTERINF;
  "EU West": DATACENTERINF;
  "EU East": DATACENTERINF;
  Poland: DATACENTERINF;
  "India East": DATACENTERINF;
  "Hong Kong": DATACENTERINF;
  Spain: DATACENTERINF;
  Chile: DATACENTERINF;
  "US Southwest": DATACENTERINF;
  "US Southeast": DATACENTERINF;
  India: DATACENTERINF;
  "EU North": DATACENTERINF;
  Emirates: DATACENTERINF;
  "US Northwest": DATACENTERINF;
  "South Africa": DATACENTERINF;
  Brazil: DATACENTERINF;
  "US Northeast": DATACENTERINF;
  "US Northcentral": DATACENTERINF;
  Japan: DATACENTERINF;
  Argentine: DATACENTERINF;
  "South Korea": DATACENTERINF;
  Singapore: DATACENTERINF;
  Australia: DATACENTERINF;
  "China Shanghai": DATACENTERINF;
  "China Tianjin": DATACENTERINF;
  "China Guangzhou": DATACENTERINF;
}

export interface API {
  result: {
    services: SERVICES | "unknown";
    datacenters: DATACENTERS | "unknown";
    matchmaking: MATCHMAKING | "unknown";
  };
}

export interface APIDEFAULT {
  result: {
    services: "unknown";
    datacenters: "unknown";
    matchmaking: "unknown";
  };
}

export enum GCConnectionStatus {
  HAVE_SESSION = 0,
  GC_GOING_DOWN = 1,
  NO_SESSION = 2,
  NO_SESSION_IN_LOGON_QUEUE = 3,
  NO_STEAM = 4,
}

export const TrueGCConnectionStatus = {
  0: "has_session",
  1: "going_down",
  2: "no_session",
  3: "no_session_in_logon_queue",
  4: "no_steam",
};

export interface GC {
  result: {
    game_coordinator: string;
  };
}
