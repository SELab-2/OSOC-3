import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../../contexts/auth-context";
import { Role } from "../../data/enums";

/**
 * React component for admin-only routes
 * Goes to login page if not authenticated, and to 403
 * if not admin
 */
export default function AdminRoute() {
    const { isLoggedIn, role } = useAuth();
    return !isLoggedIn ? (
        <Navigate to={"/"} />
    ) : role === Role.COACH ? (
        <Navigate to={"/403-forbidden"} />
    ) : (
        <Outlet />
    );
}
