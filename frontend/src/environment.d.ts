// Extending type of process.env
declare global {
    namespace NodeJS {
        interface ProcessEnv {
            REACT_APP_BASE_URL: string;
            REACT_APP_GITHUB_CLIENT_ID: string;
            REACT_APP_GITHUB_REDIRECT_URI: string;
        }
    }
}

export {};
