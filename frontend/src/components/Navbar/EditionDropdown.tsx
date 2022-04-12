import React from "react";
import NavDropdown from "react-bootstrap/NavDropdown";
import { StyledDropdownItem } from "./styles";
import { useLocation, useNavigate } from "react-router-dom";
import { getCurrentEdition, setCurrentEdition } from "../../utils/session-storage";
import { getBestRedirect } from "../../utils/logic";

interface Props {
    editions: string[];
}

/**
 * Dropdown in the [[Navbar]] to change the current edition to another one
 */
export default function EditionDropdown(props: Props) {
    const navItems: React.ReactNode[] = [];
    const location = useLocation();
    const navigate = useNavigate();

    // User can't access any editions yet, no point in rendering the dropdown either
    // as it would just show "UNDEFINED" at the top
    if (props.editions.length === 0) {
        return null;
    }

    // If anything went wrong loading the edition, default to the first one
    // found in the list of editions
    // This shouldn't happen, but just in case
    // The list can never be empty because then we return null above ^
    const currentEdition = getCurrentEdition() || props.editions[0];

    /**
     * Change the route based on the edition
     * This can't be a separate function because it uses hooks which may
     * only be used in React components
     */
    function handleSelect(edition: string) {
        const destination = getBestRedirect(location, edition);
        setCurrentEdition(edition);

        navigate(destination);
    }

    // Load dropdown items dynamically
    props.editions.forEach((edition: string) => {
        navItems.push(
            <StyledDropdownItem
                key={edition}
                active={currentEdition === edition}
                onClick={() => handleSelect(edition)}
            >
                {edition}
            </StyledDropdownItem>
        );
    });

    return <NavDropdown title={`Edition ${currentEdition}`}>{navItems}</NavDropdown>;
}
