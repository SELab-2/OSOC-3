import React from "react";
import logo from "./logo.svg";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";
import "./Buttons.css";

function App() {
    return (
        <div className="App">
            <header className="App-header">
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
                <button prefix="e-icon e-handup" className="red_login_button">
                    Github
                    <span></span>
                </button>
            </header>
        </div>
    );
}

export default App;
