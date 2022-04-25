import { GithubLoginButton } from "react-social-login-buttons";
import { Socials, SocialsContainer } from "./styles";
import { GITHUB_CLIENT_ID } from "../../../settings";
import { createRedirectUri } from "../../../utils/logic";
import { OAuthProvider } from "../../../data/enums";

export default function SocialButtons(props: { edition: string; uuid: string }) {
    async function githubRegister() {
        let authUrl = `https://github.com/login/oauth/authorize?client_id=${GITHUB_CLIENT_ID}`;
        authUrl += `&redirect_uri=${encodeURIComponent(
            createRedirectUri(OAuthProvider.GITHUB, props)
        )}`;
        authUrl += "&scope=read:user%20user:email";

        window.location.replace(authUrl);
    }

    return (
        <SocialsContainer>
            <Socials>
                <GithubLoginButton text="Register with Github" onClick={githubRegister} />
            </Socials>
        </SocialsContainer>
    );
}
