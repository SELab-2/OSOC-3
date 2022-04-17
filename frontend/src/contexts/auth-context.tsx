/** Context hook to maintain the authentication state of the user **/
import { Role } from "../data/enums";
import React, { ReactNode, useContext, useState } from "react";

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

const AuthContext = React.createContext<AuthContextState>(authDefaultState());

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
