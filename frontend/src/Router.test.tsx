import { defaultAuthState } from "./tests/utils/contexts";
import { screen } from "@testing-library/react";
import { contextRender } from "./tests/utils/renderer";

test("isLoggedIn === null shows VerificationPage", () => {
    const state = defaultAuthState();

    contextRender(state);
    expect(screen.getByTestId("verifying-page")).not.toBeNull();
});

test("isLoggedIn === false shows LoginPage", () => {
    const state = defaultAuthState();
    state.isLoggedIn = false;

    contextRender(state);
    expect(screen.getByTestId("login-page")).not.toBeNull();
});
