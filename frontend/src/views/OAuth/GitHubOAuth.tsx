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
        async function tryLogIn() {
            // No code in the query parameters
            if (!searchParams.has("code")) {
                await setLoading(false);
                await setShowError(true);
                return;
            }

            const response = await logInGitHub(authCtx, searchParams.get("code")!);
            await setLoading(false);
            if (!response) {
                await setShowError(true);
            }
        }

        tryLogIn();
        // We don't want to update when the "loading" and "authCtx" dependencies change
        // because this creates an infinite loop, so we ignore the eslint warning
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [searchParams]);

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
