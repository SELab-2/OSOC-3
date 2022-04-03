import { WelcomeTextContainer } from "./styles";

/**
 * Text displayed on the [[LoginPage]] to welcome the users to the application.
 */
export default function WelcomeText() {
    return (
        <WelcomeTextContainer>
            <h1 className={"mb-5"}>Hi!</h1>
            <h3>
                Welcome to the Open Summer of Code selections app. After you've logged in with your
                account, we'll enable your account so you can get started. An admin will verify you
                as soon as possible.
            </h3>
        </WelcomeTextContainer>
    );
}
