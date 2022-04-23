/**
 * Enum for the keys in LocalStorage.
 */
export const enum LocalStorageKey {
    /**
     * Bearer token used to authorize the user's requests in the backend.
     */
    ACCESS_TOKEN = "accessToken",
    REFRESH_TOKEN = "refreshToken",
    REFRESH_TOKEN_LOCK = "refreshTokenLock",
}
