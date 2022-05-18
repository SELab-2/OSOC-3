import { Draggable } from "react-beautiful-dnd";
import { useParams } from "react-router-dom";
import { useAuth } from "../../../../contexts";
import { Role } from "../../../../data/enums";
import { ProjectRole, ProjectRoleSuggestion } from "../../../../data/interfaces/projects";
import { deleteStudentFromProject } from "../../../../utils/api/projectStudents";
import { DeleteButton } from "../../../Common/Buttons";
import { DrafterContainer, NameDeleteContainer, SuggestionContainer } from "./styles";

export default function SuggestedStudent({
    suggestion,
    projectRole,
    index,
}: {
    suggestion: ProjectRoleSuggestion;
    projectRole: ProjectRole;
    index: number;
}) {
    const params = useParams();
    const projectId = parseInt(params.projectId!);
    const editionId = params.editionId!;

    const { role, userId } = useAuth();

    return (
        <Draggable
            draggableId={
                suggestion.student.studentId.toString() + projectRole.projectRoleId.toString()
            }
            index={index}
            key={index}
        >
            {(provided, snapshot) => (
                <SuggestionContainer
                    ref={provided.innerRef}
                    {...provided.draggableProps}
                    {...provided.dragHandleProps}
                >
                    <NameDeleteContainer>
                        {suggestion.student.firstName + " " + suggestion.student.lastName}
                        {(role === Role.ADMIN || userId === suggestion.drafter.userId) && (
                            <DeleteButton
                                onClick={() => {
                                    deleteStudentFromProject(
                                        editionId,
                                        projectId.toString(),
                                        projectRole.projectRoleId.toString(),
                                        suggestion.student.studentId.toString()
                                    );
                                }}
                            />
                        )}
                    </NameDeleteContainer>
                    <DrafterContainer>
                        {suggestion.drafter && suggestion.argumentation !== "" ? (
                            <>
                                By {suggestion.drafter.name}:{" " + suggestion.argumentation}
                            </>
                        ) : (
                            suggestion.drafter && <>By {suggestion.drafter.name}</>
                        )}
                    </DrafterContainer>
                </SuggestionContainer>
            )}
        </Draggable>
    );
}
