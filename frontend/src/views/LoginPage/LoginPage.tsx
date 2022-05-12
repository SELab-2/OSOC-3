import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { logIn } from "../../utils/api/login";

import CreateButton from "../../components/Common/Buttons/CreateButton";
import { Email, Password, SocialButtons, WelcomeText } from "../../components/LoginComponents";

import {
    EmailLoginContainer,
    LoginContainer,
    LoginPageContainer,
    NoAccount,
    VerticalDivider,
} from "./styles";
import { useAuth } from "../../contexts";

/**
 * Page where users can log in to the application.
 */
export default function LoginPage() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const authCtx = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        // If the user is already logged in, redirect them to
        // the "editions" page instead of showing the login page
        if (authCtx.isLoggedIn) {
            navigate("/editions");
        }
    }, [authCtx.isLoggedIn, navigate]);

    async function callLogIn() {
        try {
            const response = await logIn(authCtx, email, password);
            if (response) navigate("/editions");
            else alert("Something went wrong when login in");
        } catch (error) {
            console.log(error);
        }
    }

    return (
        <div data-testid={"login-page"}>
            <LoginPageContainer>
                <WelcomeText />
                <LoginContainer>
                    <SocialButtons />
                    <VerticalDivider />
                    <EmailLoginContainer>
                        <Email email={email} setEmail={setEmail} />
                        <Password
                            password={password}
                            setPassword={setPassword}
                            callLogIn={callLogIn}
                        />
                        <NoAccount>
                            Don't have an account? Ask an admin for an invite link
                        </NoAccount>
                        <div>
                            <CreateButton onClick={callLogIn} label={"Log In"} showIcon={false} />
                        </div>
                    </EmailLoginContainer>
                </LoginContainer>
            </LoginPageContainer>
        </div>
    );
}
