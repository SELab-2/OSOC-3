import { Title, TitleContainer, Cancel, TitleInput, Edit, EditDeleteContainer } from "./styles";

import { MdOutlineEditNote } from "react-icons/md";
import { Role } from "../../../data/enums/role";
import { Project } from "../../../data/interfaces/projects";
import { CreateButton, DeleteButton } from "../../Common/Buttons";

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
    editProject: () => Promise<void>;
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
                            <MdOutlineEditNote size={"35px"} onClick={() => setEditing(true)} />
                        </Edit>
                    ) : (
                        <>
                            <CreateButton
                                label="save"
                                showIcon={false}
                                onClick={async () => {
                                    await editProject();
                                    setEditing(false);
                                }}
                            />
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
                    <DeleteButton onClick={handleShow} />
                </EditDeleteContainer>
            )}
        </TitleContainer>
    );
}
