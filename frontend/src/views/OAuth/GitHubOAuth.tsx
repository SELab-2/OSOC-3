/**
 * Page displayed while GitHub auth is validating your response code
 */
import { Navigate, useSearchParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { logInGitHub } from "../../utils/api/login";
import { useAuth } from "../../contexts";
import { PageContainer, CenterText } from "../../App.styles";

export default function GitHubOAuth() {
    const authCtx = useAuth();
    const [searchParams] = useSearchParams();
    const [loading, setLoading] = useState(true);
    const [showError, setShowError] = useState(false);

    useEffect(() => {
        let unmounted = false;

        async function tryLogIn() {
            // No code in the query parameters
            if (!searchParams.has("code")) {
                setLoading(false);
                setShowError(true);
                return;
            }

            // Fix memory leak: only send API call if not yet unmounted
            if (!unmounted) {
                const response = await logInGitHub(authCtx, searchParams.get("code")!);
                setLoading(false);
                if (!response) {
                    setShowError(true);
                }
            }
        }

        tryLogIn();

        return () => {
            unmounted = true;
        };
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
