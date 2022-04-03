import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../../contexts/auth-context";
import { Role } from "../../data/enums";

/**
 * React component for admin-only routes.
 * Redirects to the [[LoginPage]] (status 401) if not authenticated,
 * and to the [[ForbiddenPage]] (status 403) if not admin.
 *
 * Example usage:
 * ```ts
 * <Route path={"/path"} element={<AdminRoute />}>
 *     // These routes will only render if the user is an admin
 *     <Route path={"/"} />
 *     <Route path={"/child"} />
 * </Route>
 * ```
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
