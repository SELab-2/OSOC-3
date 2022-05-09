import { GithubLoginButton } from "react-social-login-buttons";
import { SocialsContainer, Socials } from "./styles";

/**
 * Container for the _Sign in with GitHub_ button.
 */
export default function SocialButtons() {
    return (
        <SocialsContainer>
            <Socials>
                <GithubLoginButton />
            </Socials>
        </SocialsContainer>
    );
}
