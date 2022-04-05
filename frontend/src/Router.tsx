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
import Footer from "./components/Footer";
import { useAuth } from "./contexts/auth-context";
import PrivateRoute from "./components/PrivateRoute";
import AdminRoute from "./components/AdminRoute";
import { NotFoundPage } from "./views/errors";
import ForbiddenPage from "./views/errors/ForbiddenPage";

export default function Router() {
    const { isLoggedIn } = useAuth();

    return (
        <BrowserRouter>
            <Container>
                {isLoggedIn && <NavBar />}
                <ContentWrapper>
                    {isLoggedIn === null ? (
                        // Busy verifying the access token
                        <VerifyingTokenPage />
                    ) : (
                        // Access token was checked, if it is invalid
                        // then the <PrivateRoute /> will redirect to
                        // the LoginPage
                        <Routes>
                            <Route path={"/"} element={<LoginPage />} />
                            <Route path={"/register/:uuid"} element={<RegisterPage />} />
                            <Route path={"/students"} element={<PrivateRoute />}>
                                <Route path="" element={<StudentsPage />} />
                            </Route>
                            <Route path="/users" element={<AdminRoute />}>
                                <Route path={""} element={<UsersPage />} />
                            </Route>
                            <Route path="/projects" element={<ProjectsPage />} />
                            <Route path="/pending" element={<PendingPage />} />
                            <Route path={"/403-forbidden"} element={<ForbiddenPage />} />
                            <Route path="*" element={<NotFoundPage />} />
                        </Routes>
                    )}
                </ContentWrapper>
                {isLoggedIn && <Footer />}
            </Container>
        </BrowserRouter>
    );
}
