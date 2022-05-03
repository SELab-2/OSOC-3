import {render, screen, fireEvent} from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import LoginPage from "./LoginPage"

const mockedUsedNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
    ...jest.requireActual('react-router-dom'),
    useNavigate: () => (jest.fn())
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

