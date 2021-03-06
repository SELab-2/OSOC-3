/**
 * This file contains all interfaces used for projects.
 */

import { Skill } from "./skills";
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

/**
 * Data about a single project role suggestion.
 */
export interface ProjectRoleSuggestion {
    /** The id of the suggestion */
    projectRoleSuggestionId: number;

    /** The argumentation why this student is a good fit */
    argumentation: string;

    /** The user who suggested this student */
    drafter: Coach;

    /** The suggested student */
    student: Student;
}

/**
 * Data to create a new project role suggestion.
 */
export interface AddRoleSuggestion {
    /** The argumentation why this student is a good fit */
    argumentation: string;
}

export interface AddStudentRole {
    /** The Id of the project role where to add the student */
    projectRoleId: string;

    /** The Id of the student to add */
    studentId: string;

    /** Can be used to switch the role of a student */
    switchProjectRoleId: string | undefined;
}

/**
 * Data about a project role
 */
export interface ProjectRole {
    /** The id of the project role */
    projectRoleId: number;

    /** The id of the project this role belongs to */
    projectId: number;

    /** More info about the skill */
    description: string;

    /** The skill needed for this role */
    skill: Skill;

    /** The number of positions this role has */
    slots: number;

    /** The suggested students for this role */
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

    /** An url with more info */
    infoUrl: string | null;

    /** The coaches of this project */
    coaches: Coach[];

    /** The partners of this project */
    partners: Partner[];

    /** The roles of this project */
    projectRoles: ProjectRole[];
}

/**
 * Used as a response object for multiple projects
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
    skill: Skill;

    /** More info about this skill in a specific project */
    description: string;

    /** Number of positions of this skill in a project */
    slots: number;
}

/**
 * Used when creating a new project
 */
export interface CreateProject {
    /** The name of the new project */
    name: string;

    /** An url with more info */
    info_url: string | null;

    /** The partners that belong to this project */
    partners: string[];

    /** The IDs of the users that will coach this project */
    coaches: number[];
}

export interface CreateProjectRole {
    /** The id of the skill */
    skill_id: number;

    /** More info about this skill in a specific project */
    description: string;

    /** Number of positions of this skill in a project */
    slots: number;
}
