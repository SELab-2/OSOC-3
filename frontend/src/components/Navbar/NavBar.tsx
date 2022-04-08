import Container from "react-bootstrap/esm/Container";
import BSNavbar from "react-bootstrap/Navbar";
import { useAuth } from "../../contexts/auth-context";

export default function Navbar() {
    const { isLoggedIn } = useAuth();

    // Don't render Navbar if not logged in
    if (!isLoggedIn) {
        return null;
    }

    return (
        <BSNavbar bg={"dark"} variant={"dark"}>
            <Container>
                <BSNavbar.Brand>
                    <img src={"/assets/osoc_logo_light.svg"} alt={"OSOC logo (light)"} />
                </BSNavbar.Brand>
            </Container>
        </BSNavbar>
    );
}
