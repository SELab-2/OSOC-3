import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";
import "react-toastify/dist/ReactToastify.css";
import { AuthProvider } from "./contexts";
import { ToastContainer } from "react-toastify";
import Router from "./Router";
import { SocketProvider } from "./contexts/socket-context";

/**
 * Main application component. Wraps the [[Router]] in an [[AuthProvider]] so that
 * the [[AuthContextState]] is available throughout the entire application.
 */
export default function App() {
    return (
        // AuthContext should be available in the entire application
        <AuthProvider>
            <SocketProvider>
                <Router />
                <ToastContainer position={"bottom-right"} theme={"dark"} />
            </SocketProvider>
        </AuthProvider>
    );
}
