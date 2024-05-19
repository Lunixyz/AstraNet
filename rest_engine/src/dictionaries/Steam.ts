interface OwnsFilterObject {
  excludeFree?: boolean;
  excludeShared?: boolean;
  excludeExpiring?: boolean;
}
type StoreTagNames = Record<string, { name: string; englishName: string }>;
type PublishedFileDetails = Record<string, Record<string, any>>;

interface CreateQuickInviteLinkOptions {
  inviteLimit?: number;
  inviteDuration?: number | null;
}

interface PlayedGame {
  game_id: number;
  game_extra_info: string;
}

export interface AppChanges {
  appid: number;
  change_number: number;
  needs_token: boolean;
}

export interface PackageChanges {
  packageid: number;
  change_number: number;
  needs_token: boolean;
}

interface App {
  appid: number;
  access_token: string;
}

interface Package {
  packageid: number;
  access_token: string;
}

interface AppInfo {
  changenumber: number;
  missingToken: boolean;
  appinfo: any; // too complex to describe
}

interface PackageInfo {
  changenumber: number;
  missingToken: boolean;
  packageinfo: any; // too complex to describe
}

interface RichPresence {
  status: string;
  version: string;
  time?: string;
  "game:state": string;
  steam_display: string;
  connect: string;
}

interface OwnedApp {
  appid: number;
  name: string;
  playtime_2weeks: number | null;
  playtime_forever: number;
  img_icon_url: string;
  img_logo_url: string;
  has_community_visible_stats: boolean;
  playtime_windows_forever: number;
  playtime_mac_forever: number;
  playtime_linux_forever: number;
}

interface GetUserOwnedAppsOptions {
  includePlayedFreeGames?: boolean;
  filterAppids?: number[];
  includeFreeSub?: boolean;
}

interface ProfileItem {
  communityitemid: number;
  image_small: string | null;
  image_large: string | null;
  name: string;
  item_title: string;
  item_description: string;
  appid: number;
  item_type: unknown; // could be improved
  item_class: unknown; // could be improved
  movie_webm: string;
  movie_mp4: string;
  equipped_flags: unknown; // could be improved
}

interface AccountLimitations {
  limited: boolean;
  communityBanned: boolean;
  locked: boolean;
  canInviteFriends: boolean;
}

interface Gift {
  gid: string;
  packageid: number;
  TimeCreated: Date;
  TimeExpiration: Date;
  TimeSent: Date;
  TimeAcked: Date;
  TimeRedeemed: null;
  RecipientAddress: "";
  SenderAddress: "";
  SenderName: string;
}

interface TradeRestrictions {
  steamguardRequiredDays?: number;
  newDeviceCooldownDays?: number;
  defaultPasswordResetProbationDays?: number;
  passwordResetProbationDays?: number;
  defaultEmailChangeProbationDays?: number;
  emailChangeProbationDays?: number;
}

interface TradeURL {
  token: string;
  url: string;
}

interface QuickInviteLink {
  invite_link: string;
  invite_token: string;
  invite_limit: number;
  invite_duration: number | null;
  time_created: Date;
  valid: boolean;
}

interface SteamGuardDetails {
  isSteamGuardEnabled: boolean;
  timestampSteamGuardEnabled: Date | null;
  timestampMachineSteamGuardEnabled: Date | null;
  canTrade: boolean;
  timestampTwoFactorEnabled: Date | null;
  isPhoneVerified: boolean;
}

interface CredentialChangeTimes {
  timestampLastPasswordChange: Date | null;
  timestampLastPasswordReset: Date | null;
  timestampLastEmailChange: Date | null;
}

interface AuthSecret {
  secretID: number;
  key: Buffer;
}

interface ServerQueryResponse {
  ip: string;
  port: number;
  players: number;
  gameport: number;
}

export interface ProductChanges {
  currentChangeNumber: number;
  appChanges: AppChanges;
  packageChanges: PackageChanges;
}

export interface ProductInfo {
  apps: Record<number, AppInfo>;
  packages: Record<number, PackageInfo>;
  unknownApps: number[];
  unknownPackages: number[];
}

interface ProductAccessTokens {
  appTokens: Record<string, string>;
  packageTokens: Record<string, string>;
  appDeniedTokens: number[];
  packageDeniedTokens: number[];
}

interface UserOwnedApps {
  game_count: number;
  games: OwnedApp[];
}

interface ProfileItems {
  profile_backgrounds: ProfileItem[];
  mini_profile_backgrounds: ProfileItem[];
  avatar_frames: ProfileItem[];
  animated_avatars: ProfileItem[];
  profile_modifiers: ProfileItem[];
}
