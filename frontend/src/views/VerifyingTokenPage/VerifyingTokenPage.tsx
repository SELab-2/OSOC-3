import { useContext, useEffect } from "react";
import { AuthContext } from "../../contexts";

export default function VerifyingTokenPage() {
    const authContext = useContext(AuthContext);

    useEffect(() => {
        const verifyToken = async () => {};

        verifyToken();
    }, []);

    // This will be replaced later on
    return <h1>Loading...</h1>;
}
