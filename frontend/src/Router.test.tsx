import React from "react";
import Router from "./Router";
import { defaultAuthState, TestAuthProvider } from "./tests/utils/contexts";
import { render, screen } from "@testing-library/react";

test("isLoggedIn === null shows VerificationPage", () => {
    const state = defaultAuthState();

    render(
        <TestAuthProvider state={state}>
            <Router />
        </TestAuthProvider>
    );

    expect(screen.getByTestId("verifying-page")).not.toBeNull();
});

test("isLoggedIn === false shows LoginPage", () => {
    const state = defaultAuthState();
    state.isLoggedIn = false;

    render(
        <TestAuthProvider state={state}>
            <Router />
        </TestAuthProvider>
    );

    expect(screen.getByTestId("login-page")).not.toBeNull();
});
