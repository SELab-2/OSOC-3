import { BSNavbar, HorizontalSep, VerticalSep } from "./styles";
import { useAuth } from "../../contexts";
import Nav from "react-bootstrap/Nav";
import EditionDropdown from "./EditionDropdown";
import "./Navbar.css";
import LogoutButton from "./LogoutButton";
import { getCurrentEdition, setCurrentEdition } from "../../utils/session-storage";
import { matchPath, useLocation } from "react-router-dom";
import UsersDropdown from "./UsersDropdown";
import NavbarBase from "./NavbarBase";
import { LinkContainer } from "react-router-bootstrap";
import EditionNavLink from "./EditionNavLink";
import StudentsDropdown from "./StudentsDropdown";
/**
 * Navbar component displayed at the top of the screen.
 * If the user is not signed in, this is hidden automatically.
 */
export default function Navbar() {
    const { isLoggedIn, editions, role } = useAuth();
    /**
     * Important: DO NOT MOVE THIS LINE UNDERNEATH THE RETURN!
     * Placing an early return above a React hook (in this case, useLocation) causes
     * memory leaks & other wonky issues that we'd rather avoid.
     * The hook is only used below the return, but it HAS to be called here.
     */
    const location = useLocation();

    // Only render base if not logged in
    if (!isLoggedIn) {
        return <NavbarBase />;
    }

    // User is logged in: safe to try and parse the location now

    // Try to get the editionId out of the URL if it exists
    // this can not be done using useParams() because the Navbar is not inside
    // a <Route/>
    const match = matchPath({ path: "/editions/:editionId/*" }, location.pathname);
    // This is a TypeScript shortcut for 3 if-statements
    let editionId = match && match.params && match.params.editionId;

    // Matched /editions/new path
    if (editionId === "new") {
        editionId = null;
    } else if (editionId && !editions.find(e => e.name === editionId)) {
        // If the edition was not found in the user's list of editions,
        // don't display it in the navbar!
        // This will lead to a 404 or 403 re-route either way, so keep
        // the previous/the best edition displayed in the dropdown
        editionId = null;
    }

    // If the current URL contains an edition, use that
    // if not (eg. /editions), check SessionStorage
    // otherwise, use the most-recent edition from the auth response
    const currentEdition = editionId || getCurrentEdition() || editions[0].name;

    // Set the value of the new edition in SessionStorage if useful
    if (currentEdition) {
        setCurrentEdition(currentEdition);
    }

    return (
        <NavbarBase>
            {/* Make Navbar responsive (hamburger menu) */}
            <BSNavbar.Toggle aria-controls={"responsive-navbar-nav"} />
            <BSNavbar.Collapse id={"responsive-navbar-nav"}>
                <Nav className={"ms-auto"}>
                    <EditionDropdown editions={editions} />
                    <VerticalSep className={"vr d-none d-lg-block"} />
                    <HorizontalSep className={"d-lg-none"} />
                    <LinkContainer to={"/editions"} className={"link"}>
                        <Nav.Link>Editions</Nav.Link>
                    </LinkContainer>
                    <EditionNavLink currentEdition={currentEdition}>
                        <LinkContainer to={`/editions/${currentEdition}/projects`}>
                            <Nav.Link>Projects</Nav.Link>
                        </LinkContainer>
                    </EditionNavLink>
                    <StudentsDropdown
                        isLoggedIn={isLoggedIn}
                        currentEdition={currentEdition}
                        role={role}
                    />
                    <UsersDropdown currentEdition={currentEdition} role={role} />
                    <VerticalSep className={"vr d-none d-lg-block"} />
                    <HorizontalSep className={"d-lg-none"} />
                    <LogoutButton />
                </Nav>
            </BSNavbar.Collapse>
        </NavbarBase>
    );
}
