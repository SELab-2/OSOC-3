import { GoogleLoginButton, GithubLoginButton } from "react-social-login-buttons";
import { SocialsContainer, Socials, GoogleLoginContainer } from "./styles";

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
