import { AuthContextState } from "../../contexts";
import { TestAuthProvider } from "./contexts";
import Router from "../../Router";
import React from "react";
import { render } from "@testing-library/react";

/**
 * Custom renderer that adds a custom AuthProvider that can be
 * manipulated on the fly to force different scenarios
 */
export function contextRender(state: AuthContextState) {
    render(
        <TestAuthProvider state={state}>
            <Router />
        </TestAuthProvider>
    );
}
