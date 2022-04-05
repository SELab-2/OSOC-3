import { BadInvite } from "./styles";

/**
 * Message displayed when the user tries to access a registration link
 * that doesn't exist (anymore), for example `{{BASE_URL}}/register/this-is-not-a-valid-uuid`.
 */
export default function BadInviteLink() {
    return <BadInvite>Not a valid register url.</BadInvite>;
}
