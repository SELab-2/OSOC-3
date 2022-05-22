import React from "react";
import Container from "react-bootstrap/Container";
import { BSNavbar } from "./styles";
import Brand from "./Brand";

/**
 * Base component for the Navbar that is displayed at all times to allow
 * basic navigation
 */
export default function NavbarBase({ children }: { children?: React.ReactNode }) {
    return (
        <BSNavbar>
            <Container className={"mx-5"} fluid>
                <Brand />
                {children}
            </Container>
        </BSNavbar>
    );
}
