import React from "react";
import {Nav, NavLink, Bars, NavMenu, NavBtn, NavBtnLink} from "./NavBarElementss";

function NavBar() {
    return(
        <>
            <Nav>
                <NavLink to="/students">
                    <img src={require('../../images/header_logo.png')} alt='logo'/>
                </NavLink>
                <Bars />
                <NavMenu>
                    <NavLink to="/students" activeStyle>
                        Students
                    </NavLink>
                    <NavLink to="/users" activeStyle>
                        Users
                    </NavLink>
                    <NavLink to="/projects" activeStyle>
                        Projects
                    </NavLink>
                    <NavLink to="/" activeStyle>
                        Log out
                    </NavLink>
                </NavMenu>
                <NavBtn>
                    <NavBtnLink to="/register">Register</NavBtnLink>
                </NavBtn>
            </Nav>
        </>
    )
}

export default NavBar