import React from "react";
import logo from "./logo.svg";
import "./App.css";
import "./Buttons.css";

function App() {
    const hamburger = document.querySelector(".hamburger");
    const navMenu = document.querySelector(".nav-menu");
    hamburger?.addEventListener("click", e => {
        console.log("clicked hamburger");
        console.log(hamburger.classList);
        hamburger.classList.toggle("active");
        navMenu?.classList.toggle("active");
    });

    return (
        <div className="App">
            <header className="App-header">
                <nav className="navbar">
                    <h1>Selections</h1>
                    <ul className="nav-menu">
                        <li className="nav-item">
                            <a href="#" className="nav-link">
                                Home
                            </a>
                        </li>
                        <li className="nav-item">
                            <a href="#" className="nav-link">
                                Projects
                            </a>
                        </li>
                        <li className="nav-item">
                            <a href="#" className="nav-link">
                                About
                            </a>
                        </li>
                    </ul>
                    <div className="hamburger">
                        <span className="bar"></span>
                        <span className="bar"></span>
                        <span className="bar"></span>
                    </div>
                </nav>
                <img src={logo} className="App-logo" alt="logo" />
                <h1>Open Summer Of Code</h1>
                <button className="red_login_button">
                    Mail account
                    <span></span>
                </button>
                <button className="green_login_button">
                    Google
                    <span></span>
                </button>
                <button className="red_login_button">
                    Github
                    <span></span>
                </button>
            </header>
        </div>
    );
}

export default App;
