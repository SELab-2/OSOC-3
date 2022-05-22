import { Droppable } from "react-beautiful-dnd";
import { useParams } from "react-router-dom";
import { toast } from "react-toastify";
import { ProjectRole } from "../../../data/interfaces/projects";
import { deleteProjectRole } from "../../../utils/api/projectRoles";
import { DeleteButton } from "../../Common/Buttons";
import {
    NoStudents,
    ProjectRoleContainer,
    Suggestions,
    TitleDeleteContainer,
    NumberOfStudents,
    DescriptionContainer,
    DescriptionAndStudentAmount,
} from "./styles";
import SuggestedStudent from "./SuggestedStudent";
import AddNewSkill from "./AddNewSkill";
import { isReadonlyEdition } from "../../../utils/logic";
import { useAuth } from "../../../contexts";
import { Role } from "../../../data/enums";

export default function ProjectRoles({
    projectRoles,
    setGotProject,
    role,
}: {
    projectRoles: ProjectRole[];
    setGotProject: (value: boolean) => void;
    role: Role;
}) {
    const params = useParams();
    const projectId = params.projectId!;
    const editionId = params.editionId!;
    const { editions } = useAuth();

    const isReadOnly = isReadonlyEdition(editionId, editions);

    return (
        <div>
            {projectRoles.map((projectRole, _index) => (
                <ProjectRoleContainer key={_index}>
                    <TitleDeleteContainer>
                        <h4>{projectRole.skill.name}</h4>
                        {role === Role.ADMIN && (
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
                                            success: "Successfully deleted skill",
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
                        )}
                    </TitleDeleteContainer>
                    <DescriptionAndStudentAmount>
                        <DescriptionContainer>
                            <h6>{projectRole.description}</h6>
                        </DescriptionContainer>
                        <NumberOfStudents>
                            <div
                                className={
                                    projectRole.suggestions.length > projectRole.slots
                                        ? "red"
                                        : projectRole.suggestions.length === projectRole.slots
                                        ? "green"
                                        : undefined
                                }
                            >
                                {projectRole.suggestions.length.toString() +
                                    " / " +
                                    projectRole.slots.toString()}
                            </div>
                        </NumberOfStudents>
                    </DescriptionAndStudentAmount>

                    <Droppable droppableId={projectRole.projectRoleId.toString()}>
                        {(provided, snapshot) => (
                            <Suggestions ref={provided.innerRef} {...provided.droppableProps}>
                                {projectRole.suggestions.length === 0 ? (
                                    <NoStudents>Drag students here</NoStudents>
                                ) : (
                                    projectRole.suggestions.map((sug, _index2) => (
                                        <SuggestedStudent
                                            key={_index2}
                                            suggestion={sug}
                                            projectRole={projectRole}
                                            index={_index2}
                                            setGotProject={setGotProject}
                                            notDraggable={isReadOnly}
                                        />
                                    ))
                                )}
                                {provided.placeholder}
                            </Suggestions>
                        )}
                    </Droppable>
                </ProjectRoleContainer>
            ))}
            {!isReadOnly && role === Role.ADMIN && <AddNewSkill setGotProject={setGotProject} />}
        </div>
    );
}
