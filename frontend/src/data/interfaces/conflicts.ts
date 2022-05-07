export interface ConflictProject {
    projectId: number;
    name: string;
}

export interface Student {
    firstName: string;
    lastName: string;
    studentId: number;
}

/**
 * A conflict (student with multiple projects)
 */
export interface Conflict {
    student: Student;
    projects: ConflictProject[];
}

/**
 * A list of conflicts
 */
export interface Conflicts {
    conflictStudents: Conflict[];
}
