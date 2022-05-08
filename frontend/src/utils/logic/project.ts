import { Project, CreateProject as EditProject } from "../../data/interfaces";

export default function projectToEditProject(project: Project): EditProject {
    const coachesIds: number[] = [];
    project.coaches.forEach(coach => {
        coachesIds.push(coach.userId);
    });

    const partners: string[] = [];
    project.partners.forEach(partner => {
        partners.push(partner.name);
    });

    const editProject: EditProject = {
        name: project.name,
        number_of_students: project.numberOfStudents,
        skills: [],
        partners: partners,
        coaches: coachesIds,
    };
    return editProject;
}
