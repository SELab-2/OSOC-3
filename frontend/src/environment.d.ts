// Extending type of process.env
declare global {
    namespace NodeJS {
        interface ProcessEnv {
            REACT_APP_BE_DOMAIN: string;
            REACT_APP_FE_BASE_URL: string;
            REACT_APP_GITHUB_CLIENT_ID: string;
        }
    }
}

export {};
