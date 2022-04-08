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
`;

export const LogOutText = styled(BSNavbar.Text).attrs(() => ({
    className: "ms-2",
}))`
    transition: 150ms ease-out;

    &:hover {
        cursor: pointer;
        color: rgba(255, 255, 255, 75%);
        transition: 150ms ease-in;
    }
`;
