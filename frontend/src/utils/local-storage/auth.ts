import { StorageKey } from "../../data/enums";

/**
 * Write the new value of a token into LocalStorage
 */
export function setToken(value: string | null) {
    if (value === null) {
        localStorage.removeItem(StorageKey.BEARER_TOKEN);
    } else {
        localStorage.setItem(StorageKey.BEARER_TOKEN, value);
    }
}

/**
 * Pull the user's token out of LocalStorage
 * Returns null if there is no token in LocalStorage yet
 */
export function getToken(): string | null {
    return localStorage.getItem(StorageKey.BEARER_TOKEN);
}
