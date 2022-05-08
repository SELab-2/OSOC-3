import React from "react";
import { Title, TitleContainer, Save, Cancel, Delete, TitleInput, Edit } from "./styles";

import { MdOutlineEditNote } from "react-icons/md";
import { HiOutlineTrash } from "react-icons/hi";
import { Role } from "../../../data/enums/role";
import { Project, CreateProject as EditProject } from "../../../data/interfaces/projects";
import projectToEditProject from "../../../utils/logic/project";

export default function TitleAndEdit({
    editing,
    project,
    editedProject,
    setEditedProject,
    setEditing,
    editProject,
    role,
    handleShow,
}: {
    editing: boolean;
    project: Project;
    editedProject: EditProject;
    setEditedProject: (project: EditProject) => void;
    setEditing: (editing: boolean) => void;
    editProject: () => void;
    role: Role;
    handleShow: () => void;
}) {
    return (
        <TitleContainer>
            {!editing ? (
                <Title>{project.name}</Title>
            ) : (
                <TitleInput
                    value={editedProject.name}
                    onChange={e => {
                        const newProject: Project = { ...project, name: e.target.value };
                        setEditedProject(projectToEditProject(newProject));
                    }}
                />
            )}
            {!editing ? (
                <Edit>
                    <MdOutlineEditNote size={"30px"} onClick={() => setEditing(true)} />
                </Edit>
            ) : (
                <>
                    <Save
                        onClick={async () => {
                            await editProject();
                            setEditing(false);
                        }}
                    >
                        Save
                    </Save>
                    <Cancel
                        onClick={() => {
                            setEditing(false);
                            setEditedProject(projectToEditProject(project));
                        }}
                    >
                        Cancel
                    </Cancel>
                </>
            )}
            {role === Role.ADMIN && (
                <Delete onClick={handleShow}>
                    <HiOutlineTrash size={"20px"} />
                </Delete>
            )}
        </TitleContainer>
    );
}
