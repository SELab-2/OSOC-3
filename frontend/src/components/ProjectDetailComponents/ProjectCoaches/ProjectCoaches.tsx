import { TiDeleteOutline } from "react-icons/ti";
import { CoachContainer, CoachesContainer, CoachText, RemoveButton } from "./styles";
import CoachInput from "../CoachInput";
import { Project } from "../../../data/interfaces";

export default function ProjectCoaches({
    project,
    editedProject,
    setEditedProject,
    editing,
}: {
    project: Project;
    editedProject: Project;
    setEditedProject: (project: Project) => void;
    editing: boolean;
}) {
    return (
        <CoachesContainer>
            {editedProject.coaches.map((element, _index) => (
                <CoachContainer key={_index}>
                    <CoachText>{element.name}</CoachText>
                    {editing && (
                        <RemoveButton
                            onClick={() => {
                                const newCoaches = [...editedProject.coaches];

                                newCoaches.splice(_index, 1);
                                const newProject: Project = {
                                    ...project,
                                    coaches: newCoaches,
                                };
                                setEditedProject(newProject);
                            }}
                        >
                            <TiDeleteOutline size={"20px"} />
                        </RemoveButton>
                    )}
                </CoachContainer>
            ))}
            {editing && <CoachInput project={editedProject!} setProject={setEditedProject} />}
        </CoachesContainer>
    );
}
