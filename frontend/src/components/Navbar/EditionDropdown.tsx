import React from "react";
import NavDropdown from "react-bootstrap/NavDropdown";
import { StyledDropdownItem } from "./styles";
import { useNavigate } from "react-router-dom";

interface Props {
    editions: string[];
    currentEdition: string;
    setCurrentEdition: (edition: string) => void;
}

export default function EditionDropdown(props: Props) {
    const navItems: React.ReactNode[] = [];
    const navigate = useNavigate();

    /**
     * Change the route based on the edition
     * This can't be a separate function because it uses hooks which may
     * only be used in React components
     */
    function handleSelect(edition: string) {
        // TODO: Navigate to the most specific route possible for QOL?
        //  eg. /editions/old_id/students/:id => /editions/new_id/students, etc
        navigate(`/editions/${edition}`);
    }

    // Load dropdown items dynamically
    props.editions.forEach((edition: string) => {
        navItems.push(
            <StyledDropdownItem
                key={edition}
                active={props.currentEdition === edition}
                onClick={() => handleSelect(edition)}
            >
                {edition}
            </StyledDropdownItem>
        );
    });

    return <NavDropdown title={`Edition ${props.currentEdition}`}>{navItems}</NavDropdown>;
}
