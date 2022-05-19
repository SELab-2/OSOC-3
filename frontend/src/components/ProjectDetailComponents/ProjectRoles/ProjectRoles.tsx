import { Droppable } from "react-beautiful-dnd";
import { useParams } from "react-router-dom";
import { toast } from "react-toastify";
import { ProjectRole } from "../../../data/interfaces/projects";
import { deleteProjectRole } from "../../../utils/api/projectRoles";
import { DeleteButton } from "../../Common/Buttons";
import { NoStudents, ProjectRoleContainer, Suggestions, TitleDeleteContainer } from "./styles";
import SuggestedStudent from "./SuggestedStudent";
import AddNewSkill from "./AddNewSkill";

export default function ProjectRoles({
    projectRoles,
    setGotProject,
}: {
    projectRoles: ProjectRole[];
    setGotProject: (value: boolean) => void;
}) {
    const params = useParams();
    const projectId = params.projectId!;
    const editionId = params.editionId!;

    return (
        <div>
            {projectRoles.map((projectRole, _index) => (
                <ProjectRoleContainer key={_index}>
                    <TitleDeleteContainer>
                        <h4>{projectRole.skill.name}</h4>
                        <DeleteButton
                            onClick={async () => {
                                await toast.promise(
                                    deleteProjectRole(
                                        editionId,
                                        projectId,
                                        projectRole.projectRoleId.toString()
                                    ),
                                    {
                                        pending: "Deleting project role",
                                        success: "Successfully deleted project role",
                                        error: "Something went wrong",
                                    },
                                    {
                                        toastId:
                                            "deleteProjectRole" +
                                            projectRole.projectRoleId.toString(),
                                    }
                                );
                                setGotProject(false);
                            }}
                        />
                    </TitleDeleteContainer>

                    <h6>{projectRole.description}</h6>
                    {projectRole.suggestions.length.toString() +
                        " / " +
                        projectRole.slots.toString()}

                    <Droppable droppableId={projectRole.projectRoleId.toString()}>
                        {(provided, snapshot) => (
                            <Suggestions ref={provided.innerRef} {...provided.droppableProps}>
                                {projectRole.suggestions.map((sug, _index2) => (
                                    <SuggestedStudent
                                        key={_index2}
                                        suggestion={sug}
                                        projectRole={projectRole}
                                        index={_index2}
                                        setGotProject={setGotProject}
                                    />
                                ))}
                                {projectRole.suggestions.length === 0 && (
                                    <NoStudents>Drag students here</NoStudents>
                                )}
                                {provided.placeholder}
                            </Suggestions>
                        )}
                    </Droppable>
                </ProjectRoleContainer>
            ))}
            <AddNewSkill setGotProject={setGotProject} />
        </div>
    );
}
