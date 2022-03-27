import React, { useContext } from "react";
import { AuthContext } from "./contexts";
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

export default function Router() {
    const authContext = useContext(AuthContext);

    return (
        // If the user IS logged in, render the actual app
        <BrowserRouter>
            <Container>
                <NavBar token={authContext.token} setToken={authContext.setToken} />
                <ContentWrapper>
                    {authContext.isLoggedIn === null ? (
                        // Busy verifying the access token
                        <VerifyingTokenPage />
                    ) : !authContext.isLoggedIn ? (
                        // User is not logged in -> go to login page
                        <LoginPage />
                    ) : (
                        // Logged in -> show app
                        <Routes>
                            <Route
                                path="/"
                                element={<LoginPage setToken={authContext.setToken} />}
                            />
                            <Route path="/register/:uuid" element={<RegisterPage />} />
                            <Route path="/students" element={<StudentsPage />} />
                            <Route path="/users" element={<UsersPage />} />
                            <Route path="/projects" element={<ProjectsPage />} />
                            <Route path="/pending" element={<PendingPage />} />
                            <Route path="*" element={<ErrorPage />} />
                        </Routes>
                    )}
                </ContentWrapper>
                <Footer />
            </Container>
        </BrowserRouter>
    );
}
