import { FormEvent, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { logIn } from "../../utils/api/login";

import CreateButton from "../../components/Common/Buttons/CreateButton";
import { SocialButtons, WelcomeText } from "../../components/LoginComponents";

import {
    EmailLoginContainer,
    LoginContainer,
    LoginPageContainer,
    NoAccount,
    VerticalDivider,
} from "./styles";
import { useAuth } from "../../contexts";
import { FormControl } from "../../components/Common/Forms";
import FloatingLabel from "react-bootstrap/FloatingLabel";
import Form from "react-bootstrap/Form";
import { toast } from "react-toastify";

export enum ToastId {
    EmptyEmail = "login-empty-email",
    EmptyPassword = "login-empty-password",
    PendingRequest = "login-pending-request",
}

/**
 * Page where users can log in to the application.
 */
export default function LoginPage() {
    const [email, setEmail] = useState("");
    const [emailValid, setEmailValid] = useState(true);
    const [password, setPassword] = useState("");
    const [passwordValid, setPasswordValid] = useState(true);
    const authCtx = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        // If the user is already logged in, redirect them to
        // the "editions" page instead of showing the login page
        if (authCtx.isLoggedIn) {
            navigate("/editions");
        }
    }, [authCtx.isLoggedIn, navigate]);

    async function handleSubmit(event: FormEvent) {
        event.preventDefault();

        // Show error messages & form validation when email or password are empty
        if (!email) {
            toast.error("Email address cannot be empty.", { toastId: ToastId.EmptyEmail });
            setEmailValid(false);
        }

        if (!password) {
            toast.error("Password cannot be empty.", { toastId: ToastId.EmptyPassword });
            setPasswordValid(false);
        }

        if (email && password) {
            toast.dismiss();
            await toast.promise(
                callLogIn,
                {
                    pending: "Logging in...",
                },
                { toastId: ToastId.PendingRequest }
            );
        }
    }

    async function callLogIn() {
        const status = await logIn(authCtx, email, password);
        toast.dismiss();

        if (status === 200) {
            navigate("/editions");
        } else if (status === 401) {
            toast.error("Invalid email/password combination.");
            setEmailValid(false);
            setPasswordValid(false);
        } else {
            toast.warning("Something went wrong on our side.");
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
                        <Form onSubmit={handleSubmit}>
                            <FloatingLabel label={"Email address"} className={"mb-1"}>
                                <FormControl
                                    size={"lg"}
                                    placeholder={"name@example.com"}
                                    value={email}
                                    onChange={e => {
                                        setEmailValid(true);
                                        setEmail(e.target.value);
                                    }}
                                    onFocus={() => setEmailValid(true)}
                                    isInvalid={!emailValid}
                                />
                            </FloatingLabel>
                            <FloatingLabel label={"Password"} className={"mb-3"}>
                                <FormControl
                                    size={"lg"}
                                    type={"password"}
                                    placeholder={"Password"}
                                    value={password}
                                    onChange={e => {
                                        setPasswordValid(true);
                                        setPassword(e.target.value);
                                    }}
                                    onFocus={() => setPasswordValid(true)}
                                    isInvalid={!passwordValid}
                                />
                            </FloatingLabel>
                            <NoAccount>
                                Don't have an account? Ask an admin for an invite link
                            </NoAccount>
                            <div>
                                <CreateButton
                                    label={"Log In"}
                                    showIcon={false}
                                    type={"submit"}
                                    className={"shadow-none"}
                                />
                            </div>
                        </Form>
                    </EmailLoginContainer>
                </LoginContainer>
            </LoginPageContainer>
        </div>
    );
}
