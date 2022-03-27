import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";
import { AuthContext, AuthContextState } from "./contexts";
import Router from "./Router";
import { Role } from "./data/enums";
import { getToken } from "./utils/local-storage";

function App() {
    const [isLoggedIn, setIsLoggedIn] = useState<boolean | null>(null);
    const [role, setRole] = useState<Role | null>(null);
    // Default value: check LocalStorage
    const [token, setToken] = useState<string | null>(getToken());

    // Create AuthContext value
    const authContextValue: AuthContextState = {
        isLoggedIn: isLoggedIn,
        setIsLoggedIn: setIsLoggedIn,
        role: role,
        setRole: setRole,
        token: token,
        setToken: setToken,
    };

    return (
        // AuthContext should be visible in the entire application
        <AuthContext.Provider value={authContextValue}>
            <Router />
        </AuthContext.Provider>
    );
}

export default App;
