import React from "react";
import { Nav, NavLink, Bars, NavMenu } from "./NavBarElements";
import "./navbar.css";

function NavBar({ token }: any, { setToken }: any) {
    let hidden = "nav-hidden";
    if (token) {
        hidden = "nav-links";
    }

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
                                setToken("");
                            }}
                        >
                            Log out
                        </NavLink>
                    </div>
                </NavMenu>
            </Nav>
            <div className="line-under-navbar"></div>
        </>
    );
}

export default NavBar;
