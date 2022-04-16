import React from "react";
import { AuthContext, AuthContextState } from "../../contexts/auth-context";
import "@testing-library/jest-dom";

/**
 * Initial state to return & modify before passing into the provider
 */
export function defaultAuthState(): AuthContextState {
    return {
        isLoggedIn: null,
        setIsLoggedIn: jest.fn(),
        role: null,
        setRole: jest.fn(),
        userId: null,
        setUserId: jest.fn(),
        token: null,
        setToken: jest.fn(),
        editions: [],
        setEditions: jest.fn(),
    };
}

/**
 * AuthProvider to be used in unit testing
 */

export function TestAuthProvider({
    children,
    state,
}: {
    children: React.ReactNode;
    state: AuthContextState;
}) {
    return <AuthContext.Provider value={state}>{children}</AuthContext.Provider>;
}
