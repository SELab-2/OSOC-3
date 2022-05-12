/**
 * This file contains all interfaces used in projects pages.
 */

import { Student } from "./students";

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
    /** The user's ID */
    userId: number;
    /** The name of the coach */
    name: string;
}

export interface Skill {
    skillId: number;
    name: string;
}

export interface ProjectRoleSuggestion {
    projectRoleSuggestionId: number;
    argumentation: string;
    drafter: Coach;
    student: Student;
}

export interface ProjectRole {
    projectRoleId: number;
    projectId: number;
    description: string;
    skill: Skill;
    slots: number;
    suggestions: ProjectRoleSuggestion[];
}

/**
 * Data about a project.
 * Such as a list of the partners and the coaches
 */
export interface Project {
    /** The project's ID */
    projectId: number;

    /** The name of the project */
    name: string;

    /** The coaches of this project */
    coaches: Coach[];

    /** The partners of this project */
    partners: Partner[];
}

/**
 * Used as an response object for multiple projects
 */
export interface Projects {
    /** A list of projects */
    projects: Project[];
}

/**
 * Used to add skills to a project
 */
export interface SkillProject {
    /** The name of the skill */
    skill: string;

    /** More info about this skill in a specific project */
    description: string;

    /** Number of positions of this skill in a project */
    amount: number;
}

/**
 * Used when creating a new project
 */
export interface CreateProject {
    /** The name of the new project */
    name: string;

    /** The partners that belong to this project */
    partners: string[];

    /** The IDs of the users that will coach this project */
    coaches: number[];
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
