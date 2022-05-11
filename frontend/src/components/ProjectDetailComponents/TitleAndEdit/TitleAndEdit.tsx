import React from "react";
import {
    Title,
    TitleContainer,
    Save,
    Cancel,
    Delete,
    TitleInput,
    Edit,
    EditDeleteContainer,
} from "./styles";

import { MdOutlineEditNote } from "react-icons/md";
import { HiOutlineTrash } from "react-icons/hi";
import { Role } from "../../../data/enums/role";
import { Project } from "../../../data/interfaces/projects";

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
    editedProject: Project;
    setEditedProject: (project: Project) => void;
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
                        setEditedProject(newProject);
                    }}
                />
            )}
            {role === Role.ADMIN && (
                <EditDeleteContainer>
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
                                    setEditedProject(project);
                                }}
                            >
                                Cancel
                            </Cancel>
                        </>
                    )}
                    <Delete onClick={handleShow}>
                        <HiOutlineTrash size={"20px"} />
                    </Delete>
                </EditDeleteContainer>
            )}
        </TitleContainer>
    );
}
