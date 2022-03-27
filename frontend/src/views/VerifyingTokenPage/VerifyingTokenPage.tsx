import { useContext, useEffect } from "react";
import { AuthContext } from "../../contexts";

import { setBearerToken } from "../../utils/api";
import { validateBearerToken } from "../../utils/api/auth";
import { Role } from "../../data/enums";

export default function VerifyingTokenPage() {
    const authContext = useContext(AuthContext);

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
