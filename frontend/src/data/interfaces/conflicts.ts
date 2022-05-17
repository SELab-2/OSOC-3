export interface PrSuggestion {
    projectRole: { project: { name: string; projectId: number } };
    projectRoleSuggestionId: number;
}

/**
 * A conflict (student with multiple projects)
 */
export interface Conflict {
    firstName: string;
    lastName: string;
    prSuggestions: PrSuggestion[];
    studentId: number;
}

/**
 * A list of conflicts
 */
export interface Conflicts {
    conflictStudents: Conflict[];
}
