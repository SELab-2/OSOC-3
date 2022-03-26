import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./css-files/App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import NavBar from "./components/navbar";
import LoginPage from "./views/LoginPage";
import Students from "./views/StudentsPage";
import Users from "./views/UsersPage/Users";
import ProjectsPage from "./views/ProjectsPage";
import RegisterForm from "./views/RegisterPage";
import ErrorPage from "./views/ErrorPage/ErrorPage";
import PendingPage from "./views/PendingPage";
import Footer from "./components/Footer";
import { Container, ContentWrapper } from "./app.styles";

function App() {
    const [token, setToken] = useState("");

    return (
        <Router>
            <Container>
                <NavBar token={token} setToken={setToken} />

                <ContentWrapper>
                    <Routes>
                        <Route path="/" element={<LoginPage setToken={setToken} />} />
                        <Route path="/register/:uuid" element={<RegisterForm />} />
                        <Route path="/students" element={<Students />} />
                        <Route path="/users" element={<Users />} />
                        <Route path="/projects" element={<ProjectsPage />} />
                        <Route path="/pending" element={<PendingPage />} />
                        <Route path="*" element={<ErrorPage />} />
                    </Routes>
                </ContentWrapper>
                <div>Your token: {token}</div>
                <Footer />
            </Container>
        </Router>
    );
}

export default App;
