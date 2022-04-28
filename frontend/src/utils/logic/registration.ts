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
