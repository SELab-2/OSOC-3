import { useEffect } from "react";

import { setBearerToken } from "../../utils/api";
import { validateBearerToken } from "../../utils/api/auth";
import { Role } from "../../data/enums";
import { useAuth } from "../../contexts/auth-context";

export default function VerifyingTokenPage() {
    const authContext = useAuth();

    useEffect(() => {
        const verifyToken = async () => {
            const response = await validateBearerToken(authContext.token);

            if (response === null) {
                authContext.setToken(null);
                authContext.setIsLoggedIn(false);
                authContext.setRole(null);
            } else {
                // Token was valid, use it as the default request header
                setBearerToken(authContext.token);
                authContext.setIsLoggedIn(true);
                authContext.setRole(response.admin ? Role.ADMIN : Role.COACH);
            }
        };

        // Eslint doesn't like this, but it's the React way
        verifyToken();
    }, [authContext]);

    setBearerToken("test");

    // This will be replaced later on
    return <h1>Loading...</h1>;
}
