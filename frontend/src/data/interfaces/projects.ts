/**
 * This file contains all interfaces used in projects pages.
 */

/**
 * Data about a partner.
 */
export interface Partner {
    /** The name of the partner */
    name: string;
}

/**
 * Data about a coach.
 */
export interface Coach {
    /** The name of the coach */
    name: string;

    /** The user's ID */
    userId: number;
}

/**
 * Data about a project.
 * Such as a list of the partners and the coaches
 */
export interface Project {
    /** The name of the project */
    name: string;

    /** How many students are needed for this project */
    numberOfStudents: number;

    /** The partners of this project */
    partners: Partner[];

    /** The coaches of this project */
    coaches: Coach[];

    /** The name of the edition this project belongs to */
    editionName: string;

    /** The project's ID */
    projectId: number;
}

/**
 * Used as an response object for multiple projects
 */
export interface Projects {
    /** A list of projects */
    projects: Project[];
}

/**
 * Used when creating a new project
 */
export interface CreateProject {
    /** The name of the new project */
    name: string;

    /** Number of students the project needs */
    number_of_students: number;

    /** The required skills for the project */
    skills: string[];

    /** The partners that belong to this project */
    partners: Partner[];

    /** The users that will coach this project */
    coaches: Coach[];
}

/**
 * Data about a place in a project
 */
export interface StudentPlace {
    /** Whether or not this position is filled in */
    available: boolean;

    /** The skill needed for this place */
    skill: string;

    /** The name of the student if this place is filled in */
    name: string | undefined;
}
