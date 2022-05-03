import {render, screen, fireEvent} from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import LoginPage from "./LoginPage"

const mockedUsedNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
    ...jest.requireActual('react-router-dom'),
    useNavigate: () => (jest.fn())
}));

describe("renders all components", () => {

    beforeEach(() => {
        render(<LoginPage />);
    })

    it('has an email field and it changes', () => {
        const emailField = screen.getByPlaceholderText("Email");
        expect(emailField).toHaveValue("")
        userEvent.type(emailField, "email@email.com");
        expect(emailField).toHaveValue("email@email.com")
    })

    it('has an password field and it changes', () => {
        const passwordField = screen.getByPlaceholderText("Password");
        expect(passwordField).toHaveValue("")
        userEvent.type(passwordField, "wachtwoord");
        expect(passwordField).toHaveValue("wachtwoord")
        fireEvent.keyPress(passwordField, { key: "Enter", code: 13, charCode: 13 })
    })
})

