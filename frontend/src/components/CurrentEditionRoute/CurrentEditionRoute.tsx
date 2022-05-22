import { Navigate, Outlet, useParams } from "react-router-dom";
import { useAuth } from "../../contexts";
import { Role } from "../../data/enums";
import { isReadonlyEdition } from "../../utils/logic";

/**
 * React component for editable editions and admin-only routes.
 * Redirects to the [[LoginPage]] (status 401) if not authenticated,
 * and to the [[ForbiddenPage]] (status 403) if not admin or read-only.
 *
 * Example usage:
 * ```ts
 * <Route path={"/path"} element={<CurrentEditionRoute />}>
 *     // These routes will only render if the user is an admin and is not on a read-only edition
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
    ) : role === Role.COACH || isReadonlyEdition(editionId, editions) ? (
        <Navigate to={"/403-forbidden"} />
    ) : (
        <Outlet />
    );
}
