import React from "react";
import { Container, ContentWrapper } from "./app.styles";
import { BrowserRouter, Navigate, Outlet, Route, Routes } from "react-router-dom";

import { AdminRoute, Footer, Navbar, PrivateRoute } from "./components";
import { useAuth } from "./contexts";
import {
    EditionsPage,
    LoginPage,
    PendingPage,
    ProjectsPage,
    ProjectDetailPage
    RegisterPage,
    StudentsPage,
    UsersPage,
    VerifyingTokenPage,
} from "./views";
import { ForbiddenPage, NotFoundPage } from "./views/errors";
import CreateEditionPage from "./views/CreateEditionPage";
import { Role } from "./data/enums";

/**
 * Router component to render different pages depending on the current url. Renders
 * the [[VerifyingTokenPage]] if the bearer token is still being validated.
 */
export default function Router() {
    const { isLoggedIn, role, editions } = useAuth();

    return (
        <BrowserRouter>
            <Container>
                <Navbar />
                <ContentWrapper>
                    {isLoggedIn === null ? (
                        // Busy verifying the access token
                        <VerifyingTokenPage />
                    ) : isLoggedIn && role !== Role.ADMIN && editions.length === 0 ? (
                        // If you are a coach but aren't part of any editions at all, you can't do
                        // anything in the application, so you shouldn't be able to access it either
                        <PendingPage />
                    ) : (
                        // Access token was checked, if it is invalid
                        // then the <PrivateRoute /> will redirect to
                        // the LoginPage
                        <Routes>
                            <Route path={"/"} element={<LoginPage />} />
                            {/* Redirect /login to the login page */}
                            <Route path={"/login"} element={<Navigate to={"/"} replace />} />
                            <Route path={"/register/:uuid"} element={<RegisterPage />} />
                            <Route path={"/admins"} element={<AdminRoute />}>
                                {/* TODO admins page */}
                                <Route path={""} element={<div />} />
                            </Route>
                            <Route path={"/editions"} element={<PrivateRoute />}>
                                <Route path={""} element={<EditionsPage />} />
                                <Route path={"new"} element={<AdminRoute />}>
                                    {/* TODO create edition page */}
                                    <Route path={""} element={<CreateEditionPage />} />
                                </Route>
                                <Route path={":editionId"} element={<Outlet />}>
                                    {/* TODO edition page? do we need? maybe just some nav/links? */}
                                    <Route path={""} element={<div />} />

                                    {/* Projects routes */}
                                    <Route path="projects" element={<Outlet />}>
                                        <Route path={""} element={<ProjectsPage />} />
                                        <Route path={"new"} element={<AdminRoute />}>
                                            {/* TODO create project page */}
                                            <Route path={""} element={<div />} />
                                        </Route>
                                        {/* TODO project page */}
                                        <Route
                                            path={":projectId"}
                                            element={<ProjectDetailPage />}
                                        />
                                    </Route>

                                    {/* Students routes */}
                                    <Route path={"students"} element={<StudentsPage />} />
                                    {/* TODO student page */}
                                    <Route path={"students/:id"} element={<div />} />
                                    {/* TODO student emails page */}
                                    <Route path={"students/:id/emails"} element={<div />} />

                                    {/* Users routes */}
                                    <Route path="users" element={<AdminRoute />}>
                                        <Route path={""} element={<UsersPage />} />
                                    </Route>
                                </Route>
                            </Route>
                            <Route path="/pending" element={<PendingPage />} />
                            <Route path={"/403-forbidden"} element={<ForbiddenPage />} />
                            <Route path={"/404-not-found"} element={<NotFoundPage />} />
                            <Route path="*" element={<Navigate to={"/404-not-found"} replace />} />
                        </Routes>
                    )}
                </ContentWrapper>
                {isLoggedIn && <Footer />}
            </Container>
        </BrowserRouter>
    );
}
