import { LocalStorageKey } from "../../data/enums";

/**
 * Function to set a new value for the access token in LocalStorage.
 */
export function setAccessToken(value: string | null) {
    setToken(LocalStorageKey.ACCESS_TOKEN, value);
}

/**
 * Function to set a new value for the refresh token in LocalStorage.
 */
export function setRefreshToken(value: string | null) {
    setToken(LocalStorageKey.REFRESH_TOKEN, value);
}

/**
 * Function to set a new value for the refresh token lock in LocalStorage.
 */
export function setRefreshTokenLock(value: boolean | null) {
    setToken(LocalStorageKey.REFRESH_TOKEN_LOCK, value ? "TRUE" : "FALSE");
}

function setToken(key: LocalStorageKey, value: string | null) {
    if (value === null) {
        localStorage.removeItem(key);
    } else {
        localStorage.setItem(key, value);
    }
}

/**
 * Function to pull the user's access token out of LocalStorage.
 * Returns `null` if there is no token in LocalStorage yet.
 */
export function getAccessToken(): string | null {
    return getToken(LocalStorageKey.ACCESS_TOKEN);
}

/**
 * Function to pull the user's refresh token out of LocalStorage.
 * Returns `null` if there is no token in LocalStorage yet.
 */
export function getRefreshToken(): string | null {
    return getToken(LocalStorageKey.REFRESH_TOKEN);
}

/**
 * Function to check the refresh token lock in LocalStorage.
 * Returns `null` if there is no value in LocalStorage yet.
 */
export function getRefreshTokenLock(): boolean {
    return getToken(LocalStorageKey.REFRESH_TOKEN_LOCK) === "TRUE";
}

function getToken(key: LocalStorageKey) {
    return localStorage.getItem(key);
}
