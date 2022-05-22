export const BE_DOMAIN: string = process.env.REACT_APP_BE_DOMAIN || "localhost:8000";
export const secure = BE_DOMAIN.startsWith("localhost") ? "" : "s";
export const BE_BASE_URL: string = `http${secure}://${BE_DOMAIN}`; // HTTPS if not localhost
export const FE_BASE_URL: string = process.env.REACT_APP_FE_BASE_URL || "http://localhost:3000";
export const GITHUB_CLIENT_ID: string =
    process.env.REACT_APP_GITHUB_CLIENT_ID || "create_an_env_variable";
