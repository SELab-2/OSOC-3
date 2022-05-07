import { Conflict } from "../../../data/interfaces";
import { ListLink } from "./styles";

/**
 * A list-item which contains a student and all his assigned projects
 */
export default function ConflictDiv(props: { editionId: string; conflict: Conflict }) {
    return (
        <li>
            <ListLink
                to={`/editions/${props.editionId}/students/${props.conflict.student.studentId}`}
            >
                {`${props.conflict.student.firstName} ${props.conflict.student.lastName}`}
            </ListLink>
            <ul>
                {props.conflict.projects.map(conflictProject => (
                    <li key={conflictProject.projectId}>
                        <ListLink
                            to={`/editions/${props.editionId}/projects/${conflictProject.projectId}`}
                        >
                            {conflictProject.name}
                        </ListLink>
                    </li>
                ))}
            </ul>
            <br />
        </li>
    );
}
