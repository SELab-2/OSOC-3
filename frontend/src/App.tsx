import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";
import Router from "./Router";
import { AuthProvider } from "./contexts";

/**
 * Main application component. Wraps the [[Router]] in an [[AuthProvider]] so that
 * the [[AuthContextState]] is available throughout the entire application.
 */
export default function App() {
    return (
        // AuthContext should be available in the entire application
        <AuthProvider>
            <Router />
        </AuthProvider>
    );
}
