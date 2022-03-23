import React from "react";
import { Nav, NavLink, Bars, NavMenu } from "./NavBarElementss";

function NavBar() {
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
                    <div className="nav-links-hidden">
                        <NavLink to="/students">Students</NavLink>
                        <NavLink to="/users">Users</NavLink>
                        <NavLink to="/projects">Projects</NavLink>
                        <NavLink to="/">Log out</NavLink>
                    </div>
                </NavMenu>
            </Nav>
        </>
    );
}

export default NavBar;
