import { TiDeleteOutline } from "react-icons/ti";
import { StudentPlace } from "../../../data/interfaces/projects";
import { StudentPlaceContainer, AddStudent } from "./styles";

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
