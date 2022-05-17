export const BE_DOMAIN: string = process.env.REACT_APP_BE_DOMAIN || "localhost:8000";
export const BE_BASE_URL: string = `http${
    BE_DOMAIN.startsWith("localhost") ? "" : "s" // HTTPS if not localhost
}://${BE_DOMAIN}`;
export const FE_BASE_URL: string = process.env.REACT_APP_FE_BASE_URL || "http://localhost:3000";
export const GITHUB_CLIENT_ID: string =
    process.env.REACT_APP_GITHUB_CLIENT_ID || "create_an_env_variable";
