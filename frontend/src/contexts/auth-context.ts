/** Context hook to maintain the authentication state of the user **/
import { Role } from "../data/enums";
import React from "react";
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

// Set isLoggedIn to null on startup while we verify the token of the user
export const AuthContext = React.createContext<AuthContextState>(authDefaultState());
