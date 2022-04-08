import styled from "styled-components";
import Navbar from "react-bootstrap/Navbar";
import NavDropdown from "react-bootstrap/NavDropdown";

export const BSNavbar = styled(Navbar).attrs(() => ({
    collapseOnSelect: true,
    expand: "lg",
    variant: "dark",
}))`
    background-color: var(--osoc_blue);
    width: 100vw;
`;

export const BSBrand = styled(BSNavbar.Brand)`
    font-weight: bold;
`;

export const StyledDropdownItem = styled(NavDropdown.Item)`
    color: white;
    transition: 200ms ease-out;
    background-color: transparent;

    &:hover {
        background-color: transparent;
        color: var(--osoc_green);
        transition: 200ms ease-in;
    }

    &:active {
        background-color: transparent;
        color: var(--osoc_orange);
        text-decoration: underline;
        font-weight: bold;
    }
`;
