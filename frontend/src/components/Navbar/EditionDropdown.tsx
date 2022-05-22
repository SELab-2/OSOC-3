import React, { useEffect } from "react";
import NavDropdown from "react-bootstrap/NavDropdown";
import { StyledDropdownItem, DropdownLabel } from "./styles";
import { useLocation, useNavigate } from "react-router-dom";
import { getCurrentEdition, setCurrentEdition } from "../../utils/session-storage";
import { getBestRedirect } from "../../utils/logic";
import { Edition } from "../../data/interfaces";

interface Props {
    editions: Edition[];
}

/**
 * Dropdown in the [[Navbar]] to change the current edition to another one
 */
export default function EditionDropdown(props: Props) {
    const navItems: React.ReactNode[] = [];
    const location = useLocation();
    const navigate = useNavigate();

    useEffect(() => {}, []);

    // User can't access any editions yet, no point in rendering the dropdown either
    // as it would just show "UNDEFINED" at the top
    if (props.editions.length === 0) {
        return null;
    }

    // User can only access one edition, just show the label
    // Don't make it a dropdown & don't make it clickable
    if (props.editions.length === 1) {
        return <DropdownLabel className={"my-auto"}>{props.editions[0].name}</DropdownLabel>;
    }

    // If anything went wrong loading the edition, default to the first one
    // found in the list of editions
    // This shouldn't happen, but just in case
    // The list can never be empty because then we return null above ^
    const currentEdition = getCurrentEdition() || props.editions[0].name;

    /**
     * Change the route based on the edition
     * This can't be a separate function because it uses hooks which may
     * only be used in React components
     */
    function handleSelect(edition: string) {
        const destination = getBestRedirect(location.pathname, edition);
        setCurrentEdition(edition);

        navigate(destination);
    }

    // Load dropdown items dynamically
    props.editions.forEach((edition: Edition) => {
        navItems.push(
            <StyledDropdownItem
                key={edition.name}
                active={currentEdition === edition.name}
                onClick={() => handleSelect(edition.name)}
            >
                {edition.name}
            </StyledDropdownItem>
        );
    });

    return <NavDropdown title={currentEdition}>{navItems}</NavDropdown>;
}
