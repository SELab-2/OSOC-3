import React from "react";
import { render, screen } from "@testing-library/react";
import App from "./App";

test("renders Open Summer Of Code", () => {
    render(<App />);
    const linkElement = screen.getByText(/Open Summer Of Code/i);
    expect(linkElement).toBeInTheDocument();
});
