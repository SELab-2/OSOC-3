import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { logIn } from "../../utils/api/login";

import { WelcomeText, SocialButtons, Email, Password } from "../../components/LoginComponents";

import {
    LoginPageContainer,
    LoginContainer,
    EmailLoginContainer,
    VerticalDivider,
    NoAccount,
    LoginButton,
} from "./styles";
import "./LoginPage.css";
import { useAuth } from "../../contexts/auth-context";

function LoginPage({ setToken }: any) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const { isLoggedIn } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        // If the user is already logged in, redirect them to
        // the "students" page instead of showing the login page
        if (isLoggedIn) {
            // TODO find other homepage to go to
            //  perhaps editions?
            //  (the rest requires an edition)
            navigate("/students");
        }
    }, [navigate, isLoggedIn]);

    async function callLogIn() {
        try {
            const response = await logIn({ setToken }, email, password);
            if (response) navigate("/students");
            else alert("Something went wrong when login in");
        } catch (error) {
            console.log(error);
        }
    }

    return (
        <div>
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
                            <LoginButton onClick={callLogIn}>Log In</LoginButton>
                        </div>
                    </EmailLoginContainer>
                </LoginContainer>
            </LoginPageContainer>
        </div>
    );
}

export default LoginPage;
