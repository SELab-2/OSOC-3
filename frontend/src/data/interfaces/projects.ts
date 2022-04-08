export interface Partner {
    name: string;
}

export interface Coach {
    name: string;
    userId: number;
}

export interface Project {
    name: string;
    numberOfStudents: number;
    partners: Partner[];
    coaches: Coach[];
    editionName: string;
    projectId: number;
}