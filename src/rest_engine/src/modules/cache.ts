import type { CacheType } from "../dictionaries/Cache";

class Cache {
  private cache: CacheType = {};

  /**
   * Used to change a value inside of the cache system.
   * @param k The object's specific KEY name.
   * @param v The object's specific VALUE to update.
   */

  update(k: string, v: unknown): boolean {
    if (this.cache[k]) {
      this.cache[k].value = v;
      return true;
    }
    return false;
  }

  /**
   * Used to add a value inside of the cache system.
   * @param k The object's specific KEY name to add to cache.
   * @param v The object's specific VALUE to add to cache.
   * @param ttl The object's TIME TO LIVE (TTL) in seconds.
   */

  put(k: string, v: unknown, ttl?: number): boolean {
    this.cache[k] = {
      value: v,
      expire: ttl ? Date.now() + ttl * 1000 : null,
    };
    return true;
  }

  /**
   *
   * @param k The object's specific KEY name
   * @returns Null or the object's specific key value
   */

  get(k: string): unknown {
    const expire = this.cache[k]?.expire;

    if (!expire) return null;
    if (expire && expire > Date.now()) return this.cache[k].value;

    delete this.cache[k];
  }

  /**
   *
   * @param k The object's specific KEY name
   * @returns Null or the object's TTL (Time to Live)
   */

  getTTL(k: string): null | number {
    const expire = this.cache[k]?.expire;
    if (!expire) return null;

    return Math.max(expire - Date.now(), 0);
  }
}

export default new Cache();
