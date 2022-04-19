import { useAuth } from "../../contexts/auth-context";
import { Navigate, Outlet } from "react-router-dom";

/**
 * React component that redirects to the [[LoginPage]] if not authenticated when
 * trying to visit a route.
 *
 * Example usage:
 * ```ts
 * <Route path={"/path"} element={<PrivateRoute />}>
 *     // These routes will only render if the user is authenticated
 *     <Route path={"/"} />
 *     <Route path={"/child"} />
 * </Route>
 * ```
 */
export default function PrivateRoute() {
    const { isLoggedIn } = useAuth();
    return isLoggedIn ? <Outlet /> : <Navigate to={"/"} />;
}
