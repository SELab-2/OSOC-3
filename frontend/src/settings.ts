export const BE_BASE_URL: string = process.env.REACT_APP_BASE_URL || "http://localhost:8000";
export const FE_BASE_URL: string = process.env.REACT_APP_FE_BASE_URL || "http://localhost:3000";
export const GITHUB_CLIENT_ID: string =
    process.env.REACT_APP_GITHUB_CLIENT_ID || "create_an_env_variable";
export const GITHUB_REDIRECT_URI: string =
    process.env.REACT_APP_GITHUB_REDIRECT_URI || `${FE_BASE_URL}/oauth/github`;
