import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import LoginPage from "./LoginPage";

import "@testing-library/jest-dom";

const mockedUsedNavigate = jest.fn();

jest.mock("react-router-dom", () => ({
    ...jest.requireActual("react-router-dom"),
    useNavigate: () => mockedUsedNavigate,
}));

test("has an email field and it changes", async () => {
    render(<LoginPage />);
    const emailField = screen.getByPlaceholderText("name@example.com");
    expect(emailField).toHaveValue("");
    await userEvent.type(emailField, "email@email.com");
    expect(emailField).toHaveValue("email@email.com");
});

test("has an password field and it changes", async () => {
    render(<LoginPage />);
    const passwordField = screen.getByPlaceholderText("Password");
    expect(passwordField).toHaveValue("");
    await userEvent.type(passwordField, "wachtwoord");
    expect(passwordField).toHaveValue("wachtwoord");
});

test("has headings", () => {
    render(<LoginPage />);
    const headings = screen.getAllByRole("heading");
    expect(headings[0]).toHaveTextContent("Hi there!");
    expect(headings[1]).toHaveTextContent("Welcome to the Open Summer of Code selections app.");
    expect(headings[2]).toHaveTextContent(
        "After you've logged in with your account, we'll enable your account so you can get started. An admin will verify you as soon as possible."
    );
});
