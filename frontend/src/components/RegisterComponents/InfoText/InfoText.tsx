import { TitleText, Info } from "./styles";

/**
 * Message displayed on the [[RegisterPage]] to inform the user of what
 * to do, and provides some additional info on the registration links.
 */
export default function InfoText() {
    return (
        <div>
            <TitleText>Create an account</TitleText>
            <Info>
                Sign up with your social media account or email address. Your unique link is not
                re-usable.
            </Info>
        </div>
    );
}
