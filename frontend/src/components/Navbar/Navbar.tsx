import Container from "react-bootstrap/Container";
import { BSNavbar } from "./styles";
import { useAuth } from "../../contexts";
import Brand from "./Brand";
import Nav from "react-bootstrap/Nav";
import EditionDropdown from "./EditionDropdown";
import "./Navbar.css";
import LogoutButton from "./LogoutButton";
import { getCurrentEdition, setCurrentEdition } from "../../utils/session-storage/current-edition";
import { matchPath, useLocation } from "react-router-dom";
import UsersDropdown from "./UsersDropdown";

/**
 * Navbar component displayed at the top of the screen.
 * If the user is not signed in, this is hidden automatically.
 */
export default function Navbar() {
    const { isLoggedIn, editions } = useAuth();
    /**
     * Important: DO NOT MOVE THIS LINE UNDERNEATH THE RETURN!
     * Placing an early return above a React hook (in this case, useLocation) causes
     * memory leaks & other wonky issues that we'd rather avoid.
     * The hook is only used below the return, but it HAS to be called here.
     */
    const location = useLocation();

    // Don't render Navbar if not logged in
    if (!isLoggedIn) {
        return null;
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
    }

    // If the current URL contains an edition, use that
    // if not (eg. /editions), check SessionStorage
    // otherwise, use the most-recent edition from the auth response
    const currentEdition = editionId || getCurrentEdition() || editions[0];

    // Set the value of the new edition in SessionStorage if useful
    if (currentEdition) {
        setCurrentEdition(currentEdition);
    }

    return (
        <BSNavbar>
            <Container>
                <Brand />
                {/* Make Navbar responsive (hamburger menu) */}
                <BSNavbar.Toggle aria-controls={"responsive-navbar-nav"} />
                <BSNavbar.Collapse id={"responsive-navbar-nav"}>
                    <Nav className={"ms-auto"}>
                        <EditionDropdown editions={editions} />
                        <Nav.Link href={"/editions"}>Editions</Nav.Link>
                        <Nav.Link href={`/editions/${currentEdition}/projects`}>Projects</Nav.Link>
                        <Nav.Link href={`/editions/${currentEdition}/students`}>Students</Nav.Link>
                        <UsersDropdown currentEdition={currentEdition} />
                        <LogoutButton />
                    </Nav>
                </BSNavbar.Collapse>
            </Container>
        </BSNavbar>
    );
}
