/** Context hook to maintain the authentication state of the user **/
import { Role } from "../data/enums";
import React, { useContext, ReactNode, useState } from "react";
import { getToken } from "../utils/local-storage";

export interface AuthContextState {
    isLoggedIn: boolean | null;
    setIsLoggedIn: (value: boolean | null) => void;
    role: Role | null;
    setRole: (value: Role | null) => void;
    token: string | null;
    setToken: (value: string | null) => void;
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
    // Default value: check LocalStorage
    const [token, setToken] = useState<string | null>(getToken());

    // Create AuthContext value
    const authContextValue: AuthContextState = {
        isLoggedIn: isLoggedIn,
        setIsLoggedIn: setIsLoggedIn,
        role: role,
        setRole: setRole,
        token: token,
        setToken: setToken,
    };

    return <AuthContext.Provider value={authContextValue}>{children}</AuthContext.Provider>;
}
