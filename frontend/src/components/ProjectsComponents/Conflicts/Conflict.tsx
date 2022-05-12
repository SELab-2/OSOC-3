import { Conflict } from "../../../data/interfaces";
import { ListLink } from "./styles";

/**
 * A list-item which contains a student and all his assigned projects
 */
export default function ConflictDiv(props: { editionId: string; conflict: Conflict }) {
    return (
        <li>
            <ListLink to={`/editions/${props.editionId}/students/${props.conflict.studentId}`}>
                {`${props.conflict.firstName} ${props.conflict.lastName}`}
            </ListLink>
            <ul>
                {props.conflict.prSuggestions.map(prSuggestion => (
                    <li key={prSuggestion.projectRoleSuggestionId}>
                        <ListLink
                            to={`/editions/${props.editionId}/projects/${prSuggestion.projectRole.project.projectId}`}
                        >
                            {prSuggestion.projectRole.project.name}
                        </ListLink>
                    </li>
                ))}
            </ul>
            <br />
        </li>
    );
}
