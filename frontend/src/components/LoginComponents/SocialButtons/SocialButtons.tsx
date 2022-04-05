import { GoogleLoginButton, GithubLoginButton } from "react-social-login-buttons";
import { SocialsContainer, Socials, GoogleLoginContainer } from "./styles";

/**
 * Container for the _Sign in with Google_ and _Sign in with GitHub_ buttons.
 */
export default function SocialButtons() {
    return (
        <SocialsContainer>
            <Socials>
                <GoogleLoginContainer>
                    <GoogleLoginButton />
                </GoogleLoginContainer>
                <GithubLoginButton />
            </Socials>
        </SocialsContainer>
    );
}
