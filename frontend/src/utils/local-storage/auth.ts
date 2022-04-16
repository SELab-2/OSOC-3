import { LocalStorageKey } from "../../data/enums";

/**
 * Pull the user's token out of LocalStorage.
 * Returns `null` if there is no token in LocalStorage yet.
 */
export function getToken(): string | null {
    return localStorage.getItem(LocalStorageKey.BEARER_TOKEN);
}

/**
 * Set a new value for the bearer token in LocalStorage.
 */
export function setToken(value: string | null) {
    if (value === null) {
        localStorage.removeItem(LocalStorageKey.BEARER_TOKEN);
    } else {
        localStorage.setItem(LocalStorageKey.BEARER_TOKEN, value);
    }
}
