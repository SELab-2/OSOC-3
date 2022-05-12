export interface Student {
    alumni: boolean;
    editionId: number;
    emailAddress: string;
    finalDecision: number;
    firstName: string;
    lastName: string;
    nrOfSuggestions: NrSuggestions;
    phoneNumber: string;
    preferredName: string;
    skills: string[];
    studentId: number;
    wantsToBeStudentCoach: boolean;
}

export interface Students {
    /** A list of projects */
    students: Student[];
}

export interface NrSuggestions {
    yes: number;
    maybe: number;
    no: number;
}
