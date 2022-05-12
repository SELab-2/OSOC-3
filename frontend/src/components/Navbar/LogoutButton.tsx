import { LogOutText, LogOutTextHM } from "./styles";
import { logOut, useAuth } from "../../contexts";
import { useNavigate } from "react-router-dom";

/**
 * Button in the [[Navbar]] to log the user out
 */
export default function LogoutButton() {
    const authContext = useAuth();
    const navigate = useNavigate();

    /**
     * Log the user out
     */
    function handleLogout() {
        // Unset auth state
        logOut(authContext);

        // Redirect to login page
        navigate("/login");
    }

    return (
        <>
            <LogOutText className={"d-none d-lg-block"} onClick={handleLogout}>
                Log Out
            </LogOutText>
            <LogOutTextHM className={"d-lg-none"} onClick={handleLogout}>
                Log Out
            </LogOutTextHM>
        </>
    );
}
