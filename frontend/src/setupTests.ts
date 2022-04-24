// jest-dom adds custom jest matchers for asserting on DOM nodes.
// allows you to do things like:
// expect(element).toHaveTextContent(/react/i)
// learn more: https://github.com/testing-library/jest-dom
import "@testing-library/jest-dom";
import { configure } from "enzyme";
import Adapter from "enzyme-adapter-react-16";

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
                get: jest.fn(),
                post: jest.fn(),
            };
        },
    };
});
