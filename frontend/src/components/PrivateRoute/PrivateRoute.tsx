import { useAuth } from "../../contexts/auth-context";
import { Navigate, Outlet } from "react-router-dom";

/**
 * React component that goes to the login page if not authenticated
 */
export default function PrivateRoute() {
    const { isLoggedIn } = useAuth();
    // TODO check edition existence & access once routes have been moved over
    return isLoggedIn ? <Outlet /> : <Navigate to={"/"} />;
}
