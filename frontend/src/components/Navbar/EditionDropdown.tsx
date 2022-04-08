import React from "react";
import NavDropdown from "react-bootstrap/NavDropdown";
import { StyledDropdownItem } from "./styles";

interface Props {
    editions: string[];
    currentEdition: string;
    setCurrentEdition: (edition: string) => void;
}

export default function EditionDropdown(props: Props) {
    const navItems: React.ReactNode[] = [];

    // Load dropdown items dynamically
    props.editions.forEach((edition: string) => {
        navItems.push(
            <StyledDropdownItem href={"/"} key={edition}>
                {edition}
            </StyledDropdownItem>
        );
    });

    return <NavDropdown title={`Edition ${props.currentEdition}`}>{navItems}</NavDropdown>;
}
