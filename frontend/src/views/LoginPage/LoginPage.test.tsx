import {render, screen, fireEvent} from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import LoginPage from "./LoginPage"
//import * as MockLogin from "../../utils/api/login_api";

jest.mock('react-router-dom', () => ({
    ...jest.requireActual('react-router-dom'),
    useNavigate: () => (jest.fn())
}));

//const response = {
//    "data": ,
//    "status": 200
//};

/*
jest.mock('../../utils/api/login_api', () => ({
    ...jest.requireActual('../../utils/api/login_api'),
    _logIn: () => (jest.fn().mockResolvedValue({
        access_token: "test",
        refresh_token: "test",
        user: { editions: ['ed2022'] }
    } as LoginResponse))
}));
*/

//jest.mock("../../utils/api/login", () => {
//    const token = {
//        access_token: "test",
//        refresh_token: "test",
//        user: {editions: ['ed2022']}
//    }
//    console.log(token);
//    return true;
//})





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
})

