import React from "react";
import { Container, ContentWrapper } from "./App.styles";
import { BrowserRouter, Navigate, Outlet, Route, Routes } from "react-router-dom";
import { AdminRoute, Footer, Navbar, PrivateRoute, CurrentEditionRoute } from "./components";
import { useAuth } from "./contexts";
import {
    EditionsPage,
    CreateEditionPage,
    LoginPage,
    PendingPage,
    ProjectsPage,
    ProjectDetailPage,
    CreateProjectPage,
    StudentsPage,
    UsersPage,
    AdminsPage,
    VerifyingTokenPage,
} from "./views";
import { ForbiddenPage, NotFoundPage } from "./views/errors";
import { RegisterPage } from "./views/Registration";
import { Role } from "./data/enums";
import { GitHubOAuth } from "./views/OAuth";

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
                            <Route path={"/oauth"} element={<Outlet />}>
                                <Route path={"github"} element={<GitHubOAuth />} />
                                <Route
                                    path={"*"}
                                    element={<Navigate to={"/404-not-found"} replace />}
                                />
                            </Route>
                            {/* Redirect /login to the login page */}
                            <Route path={"/login"} element={<Navigate to={"/"} replace />} />
                            <Route path={"/register/redirect"} element={<RedirectPage />} />
                            <Route path={"/register/:uuid"} element={<RegisterPage />} />
                            {/* Catch all routes in a PrivateRoute, so you can't visit them */}
                            {/* unless you are logged in */}
                            <Route path={"*"} element={<PrivateRoute />}>
                                <Route path={"admins"} element={<AdminRoute />}>
                                    <Route path={""} element={<AdminsPage />} />
                                </Route>
                                <Route path={"editions"} element={<PrivateRoute />}>
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
                                            <Route path={"new"} element={<CurrentEditionRoute />}>
                                                {/* create project page */}
                                                <Route path={""} element={<CreateProjectPage />} />
                                            </Route>
                                            {/* project page */}
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
                                <Route path={"403-forbidden"} element={<ForbiddenPage />} />
                                <Route path={"404-not-found"} element={<NotFoundPage />} />
                                <Route
                                    path="*"
                                    element={<Navigate to={"/404-not-found"} replace />}
                                />
                            </Route>
                        </Routes>
                    )}
                </ContentWrapper>
                {isLoggedIn && <Footer />}
            </Container>
        </BrowserRouter>
    );
}
