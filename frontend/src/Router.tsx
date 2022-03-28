import React from "react";
import VerifyingTokenPage from "./views/VerifyingTokenPage";
import LoginPage from "./views/LoginPage";
import { Container, ContentWrapper } from "./app.styles";
import NavBar from "./components/navbar";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import RegisterPage from "./views/RegisterPage";
import StudentsPage from "./views/StudentsPage/StudentsPage";
import UsersPage from "./views/UsersPage";
import ProjectsPage from "./views/ProjectsPage/ProjectsPage";
import PendingPage from "./views/PendingPage";
import ErrorPage from "./views/ErrorPage";
import Footer from "./components/Footer";
import { useAuth } from "./contexts/auth-context";

export default function Router() {
    const { token, setToken, isLoggedIn } = useAuth();

    return (
        <BrowserRouter>
            <Container>
                {/* TODO don't pass token & setToken but use useAuth */}
                {isLoggedIn && <NavBar token={token} setToken={setToken} />}
                <ContentWrapper>
                    {isLoggedIn === null ? (
                        // Busy verifying the access token
                        <VerifyingTokenPage />
                    ) : !isLoggedIn ? (
                        // User is not logged in -> go to login page
                        <LoginPage />
                    ) : (
                        // If the user IS logged in, render the actual app
                        <Routes>
                            <Route path="/" element={<LoginPage setToken={setToken} />} />
                            <Route path="/register/:uuid" element={<RegisterPage />} />
                            <Route path="/students" element={<StudentsPage />} />
                            <Route path="/users" element={<UsersPage />} />
                            <Route path="/projects" element={<ProjectsPage />} />
                            <Route path="/pending" element={<PendingPage />} />
                            <Route path="*" element={<ErrorPage />} />
                        </Routes>
                    )}
                </ContentWrapper>
                {isLoggedIn && <Footer />}
            </Container>
        </BrowserRouter>
    );
}
