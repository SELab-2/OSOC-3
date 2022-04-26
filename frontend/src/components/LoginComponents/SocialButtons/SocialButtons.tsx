import { GithubLoginButton } from "react-social-login-buttons";
import { SocialsContainer, Socials } from "./styles";
import { GITHUB_CLIENT_ID, FE_BASE_URL } from "../../../settings";
import { generateRegisterState } from "../../../utils/session-storage";

/**
 * Container for the _Sign in with GitHub_ button.
 */
export default function SocialButtons() {
    async function callGitHubLogIn() {
        let authUrl = `https://github.com/login/oauth/authorize?client_id=${GITHUB_CLIENT_ID}`;
        authUrl += `&redirect_uri=${encodeURIComponent(`${FE_BASE_URL}/oauth/github`)}`;
        authUrl += `&state=${generateRegisterState()}`;

        window.location.replace(authUrl);
    }

    return (
        <SocialsContainer>
            <Socials>
                <GithubLoginButton onClick={callGitHubLogIn}/>
            </Socials>
        </SocialsContainer>
    );
}
