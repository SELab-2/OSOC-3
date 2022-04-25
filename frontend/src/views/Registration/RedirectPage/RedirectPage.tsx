import { useSearchParams } from "react-router-dom";
import { RedirectPageContainer } from "./styles";
import { useEffect, useState } from "react";
import { getRegisterState } from "../../../utils/session-storage";
import { registerGithub } from "../../../utils/api/register";

/**
 * Page where users end up after using an OAuth application
 */
export default function RedirectPage() {
    const [searchParams] = useSearchParams();
    const [showErrorMessage, setShowErrorMessage] = useState(false);
    const [loading] = useState(false);

    useEffect(() => {
        // Check if all parameters are present
        const requiredParams = ["edition", "uuid", "provider", "state", "code"];

        if (requiredParams.some(key => !searchParams.has(key))) {
            setShowErrorMessage(true);
            return;
        }

        // Check if state matches
        if (!(getRegisterState() === searchParams.get("state"))) {
            setShowErrorMessage(true);
            return;
        }

        // These can never be null as that's checked above, so the '!' is safe but
        // required to make ESLint happy
        registerGithub(
            searchParams.get("edition")!,
            searchParams.get("uuid")!,
            searchParams.get("code")!
        );
    }, [searchParams]); // searchParams never updates, but it's a state hook so this is required

    if (showErrorMessage) {
        return (
            <RedirectPageContainer>
                <h2>Uh-oh!</h2>
                <br />
                That doesn't look like a valid URI.
                <br />
                Did you fiddle with something?
            </RedirectPageContainer>
        );
    }

    if (loading) {
        return <RedirectPageContainer>Registering...</RedirectPageContainer>;
    }

    return null;
}
