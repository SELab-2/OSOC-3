import { Droppable, Draggable } from "react-beautiful-dnd";
import { ProjectRole } from "../../../data/interfaces/projects";
import { ProjectRoleContainer, SuggestionContainer, Suggestions } from "./styles";

export default function ProjectRoles({ projectRoles }: { projectRoles: ProjectRole[] }) {
    return (
        <div>
            {projectRoles.map((projectRole, _index) => (
                <ProjectRoleContainer key={_index}>
                    <h4>{projectRole.skill.name}</h4>
                    <h6>{projectRole.description}</h6>
                    {projectRole.suggestions.length.toString() +
                        " / " +
                        projectRole.slots.toString()}
                    <Droppable droppableId={projectRole.projectRoleId.toString()}>
                        {(provided, snapshot) => (
                            <Suggestions ref={provided.innerRef} {...provided.droppableProps}>
                                {projectRole.suggestions.map((sug, _index2) => (
                                    <Draggable
                                        draggableId={sug.student.studentId.toString()}
                                        index={_index2}
                                        key={_index2}
                                    >
                                        {(provided, snapshot) => (
                                            <SuggestionContainer
                                                ref={provided.innerRef}
                                                {...provided.draggableProps}
                                                {...provided.dragHandleProps}
                                            >
                                                {sug.student.firstName}
                                            </SuggestionContainer>
                                        )}
                                    </Draggable>
                                ))}
                                {provided.placeholder}
                            </Suggestions>
                        )}
                    </Droppable>
                </ProjectRoleContainer>
            ))}
        </div>
    );
}
