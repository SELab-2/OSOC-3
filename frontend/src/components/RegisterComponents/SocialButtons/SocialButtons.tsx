import { GithubLoginButton } from "react-social-login-buttons";
import { SocialsContainer, Socials } from "./styles";

export default function SocialButtons() {
    return (
        <SocialsContainer>
            <Socials>
                <GithubLoginButton text="Register with Github" />
            </Socials>
        </SocialsContainer>
    );
}
