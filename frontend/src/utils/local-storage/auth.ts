import { StorageKey } from "../../data/enums";

/**
 * Function to set a new value for the bearer token in LocalStorage.
 */
export function setToken(value: string | null) {
    if (value === null) {
        localStorage.removeItem(StorageKey.BEARER_TOKEN);
    } else {
        localStorage.setItem(StorageKey.BEARER_TOKEN, value);
    }
}

/**
 * Function to pull the user's token out of LocalStorage.
 * Returns `null` if there is no token in LocalStorage yet.
 */
export function getToken(): string | null {
    return localStorage.getItem(StorageKey.BEARER_TOKEN);
}
