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

export const Dropdown = styled(NavDropdown)`
    background-color: var(--osoc_blue);
    color: white;
`;
