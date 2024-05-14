export interface CacheType {
  [key: string]: {
    value: unknown;
    expire: number | null;
  };
}
