import { OAuthProvider } from "../../data/enums";
import { FE_BASE_URL } from "../../settings";

const Buffer = require("buffer/").Buffer;

/**
 * Decode a base64-encoded registration link
 */
export function decodeRegistrationLink(
    url: string | undefined
): { edition: string; uuid: string } | null {
    if (!url) return null;

    // Base64 decode
    const decoded = Buffer.from(url, "base64").toString();

    // Invalid link
    if (!decoded.includes("/")) {
        return null;
    }

    try {
        const [edition, uuid] = decoded.split("/");

        return {
            edition: edition,
            uuid: uuid,
        };
    } catch (e) {
        console.error(e);
        return null;
    }
}

/**
 * Compose a redirect uri for oauth providers
 */
export function createRedirectUri(
    provider: OAuthProvider,
    data: { edition: string; uuid: string }
): string {
    const encodedEdition = encodeURIComponent(data.edition);
    return `${FE_BASE_URL}/register/redirect?provider=${provider}&edition=${encodedEdition}&uuid=${data.uuid}`;
}
