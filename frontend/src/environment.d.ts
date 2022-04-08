// Extending type of process.env
declare global {
    namespace NodeJS {
        interface ProcessEnv {
            REACT_APP_BASE_URL: string;
        }
    }
}

export {};
