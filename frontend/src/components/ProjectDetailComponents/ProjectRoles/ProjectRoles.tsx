import { Droppable } from "react-beautiful-dnd";
import { ProjectRole } from "../../../data/interfaces/projects";
import { NoStudents, ProjectRoleContainer, Suggestions } from "./styles";
import SuggestedStudent from "./SuggestedStudent";

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
                                    <SuggestedStudent
                                        suggestion={sug}
                                        projectRole={projectRole}
                                        index={_index2}
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
        </div>
    );
}
