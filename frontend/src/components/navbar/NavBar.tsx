import React from "react";
import { Bars, Nav, NavLink, NavMenu } from "./NavBarElements";
import "./navbar.css";
import { useAuth } from "../../contexts/auth-context";

function NavBar() {
    const { token, setToken } = useAuth();
    const hidden = token ? "nav-links" : "nav-hidden";

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
                        <NavLink to="/editions/2023/users">Users</NavLink>
                        <NavLink
                            to="/"
                            onClick={() => {
                                setToken(null);
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

export default NavBar;
