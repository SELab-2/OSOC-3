/**
 * Page displayed while GitHub auth is validating your response code
 */
import { Navigate, useSearchParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { logInGitHub } from "../../utils/api/login";
import { useAuth } from "../../contexts";
import { PageContainer, CenterText } from "../../app.styles";

export default function GitHubOAuth() {
    const authCtx = useAuth();
    const [searchParams] = useSearchParams();
    const [loading, setLoading] = useState(true);
    const [showError, setShowError] = useState(false);

    useEffect(() => {
        // Avoid constantly re-triggering itself, tryLogIn updates authCtx
        // which will create an endless loop
        if (!loading) return;

        async function tryLogIn() {
            const response = await logInGitHub(authCtx, searchParams.get("code")!);
            setLoading(true);
            if (!response) {
                setShowError(true);
            }
        }

        if (!searchParams.has("code")) {
            setLoading(false);
            setShowError(true);
            return;
        }

        tryLogIn();
    }, [authCtx, loading, searchParams]);

    if (showError) {
        return (
            <PageContainer>
                <CenterText>
                    <h3>Invalid GitHub credentials</h3>
                </CenterText>
            </PageContainer>
        );
    }

    if (loading) {
        return (
            <PageContainer>
                <CenterText>Authenticating...</CenterText>
            </PageContainer>
        );
    }

    return <Navigate to={"/"} />;
}
