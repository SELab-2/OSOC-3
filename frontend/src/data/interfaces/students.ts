/**
 * This file contains all interfaces used in students pages.
 */

import { Skill } from "./skills";

/**
 * Data about a student.
 */
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
    skills: Skill[];
    studentId: number;
    wantsToBeStudentCoach: boolean;
}

/**
 * Used as a response object for multiple students.
 */
export interface Students {
    /** A list of students */
    students: Student[];
}

/**
 * Data to represent the amount of suggestions for each suggestion.
 */
export interface NrSuggestions {
    yes: number;
    maybe: number;
    no: number;
}
