import { Navigate, Outlet, useParams } from "react-router-dom";
import { useAuth } from "../../contexts/auth-context";
import { Role } from "../../data/enums";

/**
 * React component for current edition and admin-only routes.
 * Redirects to the [[LoginPage]] (status 401) if not authenticated,
 * and to the [[ForbiddenPage]] (status 403) if not admin or not the current edition.
 *
 * Example usage:
 * ```ts
 * <Route path={"/path"} element={<CurrentEditionRoute />}>
 *     // These routes will only render if the user is an admin and is on the current edition
 *     <Route path={"/"} />
 *     <Route path={"/child"} />
 * </Route>
 * ```
 */
export default function CurrentEditionRoute() {
    const { isLoggedIn, role, editions } = useAuth();
    const params = useParams();
    const editionId = params.editionId;
    return !isLoggedIn ? (
        <Navigate to={"/"} />
    ) : role === Role.COACH || editionId !== editions[0] ? (
        <Navigate to={"/403-forbidden"} />
    ) : (
        <Outlet />
    );
}
