import { useEffect } from "react";

import { validateBearerToken } from "../../utils/api/auth";
import { logIn, logOut, useAuth } from "../../contexts/auth-context";
import { getAccessToken, getRefreshToken } from "../../utils/local-storage";

/**
 * Placeholder page shown while the bearer token found in LocalStorage is being verified.
 * If the token is valid, redirects to the application. Otherwise, redirects to the [[LoginPage]].
 */
export default function VerifyingTokenPage() {
    const authContext = useAuth();

    useEffect(() => {
        const verifyToken = async () => {
            const accessToken = getAccessToken();
            const refreshToken = getRefreshToken();

            if (accessToken === null || refreshToken === null) {
                logOut(authContext);
                return;
            }

            const response = await validateBearerToken(accessToken);

            if (response === null) {
                logOut(authContext);
            } else {
                // Token was valid, use it as the default request header
                // and set all data in the AuthContext
                logIn(response, authContext);
            }
        };

        // Eslint doesn't like this, but it's the React way
        verifyToken();
    }, [authContext]);

    // This will be replaced later on
    return (
        <div data-testid={"verifying-page"}>
            <h1>Loading...</h1>
        </div>
    );
}
