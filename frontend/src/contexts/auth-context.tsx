/** Context hook to maintain the authentication state of the user **/
import { Role } from "../data/enums";
import React, { useContext, ReactNode, useState } from "react";
import { User } from "../data/interfaces";
import { setCurrentEdition } from "../utils/session-storage";
import { setAccessToken, setRefreshToken } from "../utils/local-storage";

/**
 * Interface that holds the data stored in the AuthContext.
 */
export interface AuthContextState {
    isLoggedIn: boolean | null;
    setIsLoggedIn: (value: boolean | null) => void;
    role: Role | null;
    setRole: (value: Role | null) => void;
    userId: number | null;
    setUserId: (value: number | null) => void;
    editions: string[];
    setEditions: (value: string[]) => void;
}

/**
 * Function to create a (placeholder) default value for the state.
 * These values are never used, but React context hooks expect a default value
 * so there is no way around it.
 */
function authDefaultState(): AuthContextState {
    return {
        isLoggedIn: null,
        setIsLoggedIn: (_: boolean | null) => {},
        role: null,
        setRole: (_: Role | null) => {},
        userId: null,
        setUserId: (_: number | null) => {},
        editions: [],
        setEditions: (_: string[]) => {},
    };
}

export const AuthContext = React.createContext<AuthContextState>(authDefaultState());

/**
 * Custom React hook to use our authentication context.
 */
export function useAuth(): AuthContextState {
    return useContext(AuthContext);
}

/**
 * Provider for auth that creates getters, setters, maintains state, and
 * provides default values.
 *
 * This keeps the main [[App]] component code clean by handling this
 * boilerplate here instead.
 */
export function AuthProvider({ children }: { children: ReactNode }) {
    const [isLoggedIn, setIsLoggedIn] = useState<boolean | null>(null);
    const [role, setRole] = useState<Role | null>(null);
    const [editions, setEditions] = useState<string[]>([]);
    const [userId, setUserId] = useState<number | null>(null);

    // Create AuthContext value
    const authContextValue: AuthContextState = {
        isLoggedIn: isLoggedIn,
        setIsLoggedIn: setIsLoggedIn,
        role: role,
        setRole: setRole,
        userId: userId,
        setUserId: setUserId,
        editions: editions,
        setEditions: setEditions,
    };

    return <AuthContext.Provider value={authContextValue}>{children}</AuthContext.Provider>;
}

/**
 * Set the user's login data in the AuthContext
 */
export function logIn(user: User, authContext: AuthContextState) {
    authContext.setUserId(user.userId);
    authContext.setRole(user.admin ? Role.ADMIN : Role.COACH);
    authContext.setEditions(user.editions);
    authContext.setIsLoggedIn(true);
}

/**
 * Remove a user's login data from the AuthContext
 */
export function logOut(authContext: AuthContextState) {
    authContext.setIsLoggedIn(false);
    authContext.setUserId(null);
    authContext.setRole(null);
    authContext.setEditions([]);

    // Remove tokens from LocalStorage
    setAccessToken(null);
    setRefreshToken(null);

    // Remove current edition from SessionStorage
    setCurrentEdition(null);
}
