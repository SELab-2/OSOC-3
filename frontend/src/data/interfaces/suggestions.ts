export interface Suggestion {
    suggestionId: number;
    coach: OsocCoach;
    suggestion: number;
    argumentation: string;
}

export interface OsocCoach {
    userId: number;
    name: string;
    admin: boolean;
    auth: Authentication;
}

export interface Authentication {
    authType: string;
    email: string;
}

export interface Suggestions {
    suggestions: Suggestion[];
}
