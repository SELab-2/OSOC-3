import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./css-files/App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import NavBar from "./components/navbar";
import LoginPage from "./views/LoginPage";
import Students from "./views/Students";
import Users from "./views/Users";
import ProjectsPage from "./views/ProjectsPage";
import RegisterForm from "./views/RegisterForm";
import ErrorPage from "./views/ErrorPage";
import PendingPage from "./views/PendingPage";

function App() {
    return (
        <Router>
            <NavBar />
            <Routes>
                <Route path="/" element={<LoginPage />} />
                <Route path="/register" element={<RegisterForm />} />
                <Route path="/students" element={<Students />} />
                <Route path="/users" element={<Users />} />
                <Route path="/projects" element={<ProjectsPage />} />
                <Route path="/pending" element={<PendingPage />} />
                <Route path="*" element={<ErrorPage />} />
            </Routes>
        </Router>
    );
}

export default App;
