import { GithubLoginButton } from "react-social-login-buttons";
import { SocialsContainer, Socials } from "./styles";
import { axiosInstance } from "../../../utils/api/api";

export default function SocialButtons() {
    async function githubRegister() {
        await axiosInstance.post("https://github.com/login/oauth/authorize");
    }

    return (
        <SocialsContainer>
            <Socials>
                <GithubLoginButton text="Register with Github" onClick={githubRegister} />
            </Socials>
        </SocialsContainer>
    );
}
