import { Droppable, Draggable } from "react-beautiful-dnd";
import { ProjectRoleContainer, SuggestionContainer, Suggestions } from "./styles";
export default function ProjectRoles({
    projectRoles,
}: {
    projectRoles: {
        skill: string;
        slots: number;
        suggestions: {
            name: string;
        }[];
    }[];
}) {
    return (
        <div>
            {projectRoles.map((projectRole, _index) => (
                <ProjectRoleContainer key={_index}>
                    {projectRole.skill}
                    <br></br>
                    {projectRole.suggestions.length.toString() +
                        " / " +
                        projectRole.slots.toString()}
                    <Droppable droppableId={projectRole.skill}>
                        {(provided, snapshot) => (
                            <Suggestions ref={provided.innerRef} {...provided.droppableProps}>
                                {projectRole.suggestions.map((sug, _index2) => (
                                    <Draggable draggableId={sug.name} index={_index2} key={_index2}>
                                        {(provided, snapshot) => (
                                            <SuggestionContainer
                                                ref={provided.innerRef}
                                                {...provided.draggableProps}
                                                {...provided.dragHandleProps}
                                            >
                                                {sug.name}
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
