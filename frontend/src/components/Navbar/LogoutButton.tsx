import { LogOutText } from "./styles";
import { useAuth } from "../../contexts/auth-context";
import { useNavigate } from "react-router-dom";

export default function LogoutButton() {
    const authContext = useAuth();
    const navigate = useNavigate();

    /**
     * Log the user out
     */
    function handleLogout() {
        // Unset auth state
        authContext.setIsLoggedIn(false);
        authContext.setEditions([]);
        authContext.setRole(null);
        authContext.setToken(null);

        // Redirect to login page
        navigate("/login");
    }

    return <LogOutText onClick={handleLogout}>Log Out</LogOutText>;
}
