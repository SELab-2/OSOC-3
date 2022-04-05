/** Context hook to maintain the authentication state of the user **/
import { Role } from "../data/enums";
import React, { useContext, ReactNode, useState } from "react";
import { getToken, setToken as setTokenInStorage } from "../utils/local-storage";

export interface AuthContextState {
    isLoggedIn: boolean | null;
    setIsLoggedIn: (value: boolean | null) => void;
    role: Role | null;
    setRole: (value: Role | null) => void;
    token: string | null;
    setToken: (value: string | null) => void;
    editions: number[];
    setEditions: (value: number[]) => void;
}

/**
 * Create a placeholder default value for the state
 */
function authDefaultState(): AuthContextState {
    return {
        isLoggedIn: null,
        setIsLoggedIn: (_: boolean | null) => {},
        role: null,
        setRole: (_: Role | null) => {},
        token: getToken(),
        setToken: (_: string | null) => {},
        editions: [],
        setEditions: (_: number[]) => {},
    };
}

const AuthContext = React.createContext<AuthContextState>(authDefaultState());

/**
 * Custom React hook to use our authentication context
 */
export function useAuth(): AuthContextState {
    return useContext(AuthContext);
}

/**
 * Provider for auth that creates getters, setters, maintains state, and
 * provides default values
 *
 * Not strictly necessary but keeps the main App clean by handling this
 * code here instead
 */
export function AuthProvider({ children }: { children: ReactNode }) {
    const [isLoggedIn, setIsLoggedIn] = useState<boolean | null>(null);
    const [role, setRole] = useState<Role | null>(null);
    const [editions, setEditions] = useState<number[]>([]);
    // Default value: check LocalStorage
    const [token, setToken] = useState<string | null>(getToken());

    // Create AuthContext value
    const authContextValue: AuthContextState = {
        isLoggedIn: isLoggedIn,
        setIsLoggedIn: setIsLoggedIn,
        role: role,
        setRole: setRole,
        token: token,
        setToken: (value: string | null) => {
            // Log the user out if token is null
            if (value === null) {
                setIsLoggedIn(false);
            }

            // Set the token in LocalStorage
            setTokenInStorage(value);
            setToken(value);
        },
        editions: editions,
        setEditions: setEditions,
    };

    return <AuthContext.Provider value={authContextValue}>{children}</AuthContext.Provider>;
}
