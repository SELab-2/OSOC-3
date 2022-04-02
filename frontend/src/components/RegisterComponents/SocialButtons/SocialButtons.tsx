import { GoogleLoginButton, GithubLoginButton } from "react-social-login-buttons";
import { SocialsContainer, Socials } from "./styles";

export default function SocialButtons() {
    return (
        <SocialsContainer>
            <Socials>
                <GoogleLoginButton text="Register with Google" />
                <GithubLoginButton text="Register with Github" />
            </Socials>
        </SocialsContainer>
    );
}
