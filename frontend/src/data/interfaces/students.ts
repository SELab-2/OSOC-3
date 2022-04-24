export interface Student {
    firstName: string;
    nrOfSuggestions: NrSuggestions;
    studentId: number;
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