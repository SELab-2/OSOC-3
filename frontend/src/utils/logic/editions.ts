import { Edition } from "../../data/interfaces";

/**
 * Check if an edition is read-only
 */
export function isReadonlyEdition(name: string | undefined, editions: Edition[]): boolean {
    if (!name) return false;
    return editions.find(e => e.name === name)?.readonly || false;
}
