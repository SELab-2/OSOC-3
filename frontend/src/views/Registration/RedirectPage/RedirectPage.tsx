import { useSearchParams } from "react-router-dom";
import { RedirectPageContainer } from "./styles";
import { useEffect, useState } from "react";
import { getRegisterState } from "../../../utils/session-storage";

/**
 * Page where users end up after using an OAuth application
 */
export default function RedirectPage() {
    const [searchParams] = useSearchParams();
    const [showErrorMessage, setShowErrorMessage] = useState(false);

    useEffect(() => {
        // Check if all parameters are present
        const requiredParams = ["edition", "uuid", "provider", "state", "code"];

        if (requiredParams.some(key => !searchParams.has(key))) {
            setShowErrorMessage(true);
        }

        // Check if state matches
        if (!(getRegisterState() === searchParams.get("state"))) {
            setShowErrorMessage(true);
        }
    }, [searchParams]);

    if (showErrorMessage) {
        return (
            <RedirectPageContainer>
                <h3>Uh oh!</h3>
                <br />
                That doesn't look like a valid URI to us.
            </RedirectPageContainer>
        );
    }

    return <RedirectPageContainer>You are being redirected</RedirectPageContainer>;
}
