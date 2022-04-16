import {StorageKey} from "../../data/enums";

/**
 * Function to set a new value for the access token in LocalStorage.
 */
export function setAccessToken(value: string | null) {
    setToken(StorageKey.ACCESS_TOKEN, value);
}

/**
 * Function to set a new value for the refresh token in LocalStorage.
 */
export function setRefreshToken(value: string | null) {
    setToken(StorageKey.REFRESH_TOKEN, value);
}

function setToken(key: StorageKey, value: string | null) {
    if (value === null) {
        localStorage.removeItem(key);
    } else {
        localStorage.setItem(key, value);
    }
}

/**
 * Function to pull the user's token out of LocalStorage.
 * Returns `null` if there is no token in LocalStorage yet.
 */
export function getAccessToken(): string | null {
    return getToken(StorageKey.ACCESS_TOKEN)
}

/**
 * Function to pull the user's token out of LocalStorage.
 * Returns `null` if there is no token in LocalStorage yet.
 */
export function getRefreshToken(): string | null {
    return getToken(StorageKey.REFRESH_TOKEN)
}

function getToken(key: StorageKey) {
    return localStorage.getItem(key);
}
