import {render, screen, fireEvent} from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import LoginPage from "./LoginPage";
import { useNavigate } from "react-router-dom";

import "@testing-library/jest-dom";
import { configure } from "enzyme";
import Adapter from "enzyme-adapter-react-16";

const token = {
    data: {
        access_token: "test",
        refresh_token: "test",
        user: { editions: ['ed2022'] }
    }
}


// Configure Enzyme adapter
configure({ adapter: new Adapter() });

// Mock Axios so the tests never make API calls

jest.mock("axios", () => {
    return {
        create: () => {
            return {
                defaults: {
                    baseURL: "",
                },
                interceptors: {
                    request: {
                        use: jest.fn(),
                    },
                    response: {
                        use: jest.fn(),
                    },
                },
                get: () => jest.fn(),
                post: () => token,
            };
        },
    };
});

const mockedUsedNavigate = jest.fn();

jest.mock('react-router-dom', () => ({
    ...jest.requireActual('react-router-dom'),
    useNavigate: () => mockedUsedNavigate,
}));


beforeEach(() => {
    render(<LoginPage />);
})


test('has an email field and it changes', () => {
    const emailField = screen.getByPlaceholderText("Email");
    expect(emailField).toHaveValue("")
    userEvent.type(emailField, "email@email.com");
    expect(emailField).toHaveValue("email@email.com")
})

test('has an password field and it changes', () => {
    const passwordField = screen.getByPlaceholderText("Password");
    expect(passwordField).toHaveValue("")
    userEvent.type(passwordField, "wachtwoord");
    expect(passwordField).toHaveValue("wachtwoord")
})

test('has headings', () => {
    const headings = screen.getAllByRole('heading')
    expect(headings[0]).toHaveTextContent("Hi!")
    expect(headings[1]).toHaveTextContent("Welcome to the Open Summer of Code selections app. After you've logged in with your account, we'll enable your account so you can get started. An admin will verify you as soon as possible.")
})

// TODO: when the toast is implemented, edit this test that you can see the toast
//test('enter on password field and login fales', () => {
//    const passwordField = screen.getByPlaceholderText("Password");
//    expect(passwordField).toHaveValue("")
//    fireEvent.keyPress(passwordField, {key: 'Enter', code: 'Enter', charCode: 13})
//})

test('enter on password field and login goes trough', async () => {
    const emailField = screen.getByPlaceholderText("Email");
    userEvent.type(emailField, "admin@ngmail.com");
    const passwordField = screen.getByPlaceholderText("Password");
    userEvent.type(passwordField, "wachtwoord");
    fireEvent.keyPress(passwordField, {key: 'Enter', code: 'Enter', charCode: 13})
    console.log(mockedUsedNavigate)
    //screen.debug()
})

