import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";
import Router from "./Router";
import { AuthProvider } from "./contexts";

function App() {
    return (
        // AuthContext should be visible in the entire application
        <AuthProvider>
            <Router />
        </AuthProvider>
    );
}

export default App;
