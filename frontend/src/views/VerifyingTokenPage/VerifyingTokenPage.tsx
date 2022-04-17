import { useEffect } from "react";

import { validateBearerToken } from "../../utils/api/auth";
import { Role } from "../../data/enums";
import { AuthContextState, useAuth } from "../../contexts/auth-context";
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
                failedVerification(authContext);
                return;
            }

            const response = await validateBearerToken(accessToken);

            if (response === null) {
                failedVerification(authContext);
            } else {
                authContext.setIsLoggedIn(true);
                authContext.setRole(response.admin ? Role.ADMIN : Role.COACH);
                authContext.setUserId(response.userId);
                authContext.setEditions(response.editions);
            }
        };

        // Eslint doesn't like this, but it's the React way
        verifyToken();
    }, [authContext]);

    // This will be replaced later on
    return <h1>Loading...</h1>;
}

function failedVerification(authContext: AuthContextState) {
    authContext.setIsLoggedIn(false);
    authContext.setRole(null);
    authContext.setEditions([]);
    authContext.setUserId(null);
}
