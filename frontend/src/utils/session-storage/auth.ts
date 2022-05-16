import { SessionStorageKey } from "../../data/enums";

/**
 * Return the random state stored from SessionStorage used in the registration process
 */
export function getRegisterState(): string | null {
    return sessionStorage.getItem(SessionStorageKey.REGISTER_STATE);
}

/**
 * Set the state in SessionStorage to something random to prevent CSRF-attacks
 */
export function generateRegisterState(): string {
    // Generate a random string
    const state = Math.random().toString(36).slice(2);
    sessionStorage.setItem(SessionStorageKey.REGISTER_STATE, state);

    return state;
}
