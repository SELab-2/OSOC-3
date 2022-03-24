import React from "react";
import { Nav, NavLink, Bars, NavMenu } from "./NavBarElementss";

function NavBar({token}: any) {
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
                {() => {if(token === ""){
                    <div className="nav-links">
                        <NavLink to="/students">Students</NavLink>
                        <NavLink to="/users">Users</NavLink>
                        <NavLink to="/projects">Projects</NavLink>
                        <NavLink to="/">Log out</NavLink>
                    </div>
                }}}
                </NavMenu>
            </Nav>
        </>
    );
}

export default NavBar;
