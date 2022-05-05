import { TiDeleteOutline } from "react-icons/ti";
import { StudentPlace } from "../../../data/interfaces/projects";
import { StudentPlaceContainer, AddStudent } from "./styles";

/**
 * TODO this needs more work and is still mostly a placeholder.
 * @param studentPlace gives some info about a specific place in a project.
 * @returns a component to add a student to a project place or to view a student added to the project.
 */
export default function StudentPlaceholder({ studentPlace }: { studentPlace: StudentPlace }) {
    if (studentPlace.available) {
        return (
            <StudentPlaceContainer>
                {studentPlace.skill}
                <AddStudent />
            </StudentPlaceContainer>
        );
    } else
        return (
            <StudentPlaceContainer>
                {studentPlace.skill}
                {" " + studentPlace.name}
                <TiDeleteOutline size={"20px"} />
            </StudentPlaceContainer>
        );
}
