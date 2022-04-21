import { SessionStorageKey } from "../../data/enums";

/**
 * Return the edition currently stored in SessionStorage.
 */
export function getCurrentEdition(): string | null {
    return sessionStorage.getItem(SessionStorageKey.CURRENT_EDITION);
}

/**
 * Set the edition in SessionStorage.
 * If `null`, the current value is removed instead.
 */
export function setCurrentEdition(edition: string | null) {
    if (edition === null) {
        sessionStorage.removeItem(SessionStorageKey.CURRENT_EDITION);
    } else {
        sessionStorage.setItem(SessionStorageKey.CURRENT_EDITION, edition);
    }
}
