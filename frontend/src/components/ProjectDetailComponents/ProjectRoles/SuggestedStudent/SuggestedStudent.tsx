import { Draggable } from "react-beautiful-dnd";
import { useNavigate, useParams } from "react-router-dom";
import { toast } from "react-toastify";
import { useAuth } from "../../../../contexts";
import { Role } from "../../../../data/enums";
import { ProjectRole, ProjectRoleSuggestion } from "../../../../data/interfaces/projects";
import { deleteStudentFromProject } from "../../../../utils/api/projectStudents";
import { DeleteButton } from "../../../Common/Buttons";
import { DrafterContainer, NameDeleteContainer, SuggestionContainer, StudentName } from "./styles";

export default function SuggestedStudent({
    suggestion,
    projectRole,
    index,
    setGotProject,
    notDraggable,
}: {
    suggestion: ProjectRoleSuggestion;
    projectRole: ProjectRole;
    index: number;
    setGotProject: (value: boolean) => void;
    notDraggable: boolean;
}) {
    const params = useParams();
    const projectId = parseInt(params.projectId!);
    const editionId = params.editionId!;

    const { role, userId } = useAuth();

    const navigate = useNavigate();

    return (
        <Draggable
            draggableId={
                suggestion.student.studentId.toString() + projectRole.projectRoleId.toString()
            }
            index={index}
            key={index}
            isDragDisabled={notDraggable}
        >
            {(provided, snapshot) => (
                <SuggestionContainer
                    ref={provided.innerRef}
                    {...provided.draggableProps}
                    {...provided.dragHandleProps}
                >
                    <NameDeleteContainer>
                        <StudentName
                            onClick={() =>
                                navigate(
                                    "/editions/" +
                                        editionId +
                                        "/students/" +
                                        suggestion.student.studentId
                                )
                            }
                        >
                            {suggestion.student.firstName + " " + suggestion.student.lastName}
                        </StudentName>
                        {(role === Role.ADMIN || userId === suggestion.drafter.userId) && (
                            <DeleteButton
                                onClick={async () => {
                                    await toast.promise(
                                        deleteStudentFromProject(
                                            editionId,
                                            projectId.toString(),
                                            projectRole.projectRoleId.toString(),
                                            suggestion.student.studentId.toString()
                                        ),
                                        {
                                            pending: "Deleting student from project",
                                            success: "Successfully removed student",
                                            error: "Something went wrong",
                                        }
                                    );
                                    setGotProject(false);
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
