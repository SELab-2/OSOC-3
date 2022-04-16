import React from "react";
import { Bars, Nav, NavLink, NavMenu } from "./NavBarElements";
import "./navbar.css";
import { useAuth } from "../../contexts/auth-context";

/**
 * NavBar displayed at the top of the page.
 * Links are hidden if the user is not authorized to see them.
 */
export default function NavBar() {
    const { accessToken, setAccessToken } = useAuth();
    const hidden = accessToken ? "nav-links" : "nav-hidden";

    return (
        <>
            <Nav>
                <div className="logo-plus-name">
                    <img
                        src={require("../../images/header_logo.png")}
                        alt="logo"
                        style={{ marginRight: "20px" }}
                    />
                    <h1> Selections</h1>
                </div>
                <Bars />

                <NavMenu>
                    <div className={hidden}>
                        <NavLink to="/students">Students</NavLink>
                        <NavLink to="/projects">Projects</NavLink>
                        <NavLink to="/users">Users</NavLink>
                        <NavLink
                            to="/"
                            onClick={() => {
                                setAccessToken(null);
                            }}
                        >
                            Log out
                        </NavLink>
                    </div>
                </NavMenu>
            </Nav>
        </>
    );
}
