import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import NavBar from "./components/navbar";
import LoginPage from "./views/LoginPage";
import StudentsPage from "./views/StudentsPage";
import UsersPage from "./views/UsersPage";
import ProjectsPage from "./views/ProjectsPage";
import RegisterPage from "./views/RegisterPage";
import ErrorPage from "./views/ErrorPage";
import PendingPage from "./views/PendingPage";
// import Footer from "./components/Footer";
import { Container, ContentWrapper } from "./app.styles";
import StudentInfoPage from "./views/StudentInfoPage";

function App() {
    const [token, setToken] = useState("");

    return (
        <Router>
            <Container>
                <NavBar token={token} setToken={setToken} />

                <ContentWrapper>
                    <Routes>
                        <Route path="/" element={<LoginPage setToken={setToken} />} />
                        <Route path="/register/:uuid" element={<RegisterPage />} />
                        <Route path="/students" element={<StudentsPage />} />
                        <Route path="/students/:studentid" element={<StudentInfoPage />} />
                        <Route path="/users" element={<UsersPage />} />
                        <Route path="/projects" element={<ProjectsPage />} />
                        <Route path="/pending" element={<PendingPage />} />
                        <Route path="*" element={<ErrorPage />} />
                    </Routes>
                </ContentWrapper>
                {/* <div>Your token: {token}</div>
                <Footer /> */}
            </Container>
        </Router>
    );
}

export default App;
