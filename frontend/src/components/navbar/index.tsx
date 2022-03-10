import React from "react";
import {Nav, NavLink, Bars, NavMenu} from "./NavBarElementss";

function NavBar() {
    return(
        <>
            <Nav>
                <div className="logo-plus-name">
                    <img src={require('../../images/header_logo.png')} alt='logo' style={{marginRight: '20px'}}/>
                    <h1> Selections</h1>
                </div>
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
            </Nav>
        </>
    )
}

export default NavBar