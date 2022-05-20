import { StudentListFilters } from "../StudentsComponents";
import StudentInformation from "./StudentInformation/StudentInformation";
import { StudentInfoPageContent } from "./styles";
import { DragDropContext } from "react-beautiful-dnd";

/**
 * Component that renders the students list and the information about the currently selected student.
 * @param props all student, current student and all filters to handle the student information page.
 */
export default function StudentInfo(props: { studentId: number; editionId: string }) {
    return (
        <StudentInfoPageContent>
            <DragDropContext onDragEnd={() => {}}>
                <StudentListFilters />
            </DragDropContext>
            <StudentInformation studentId={props.studentId} editionId={props.editionId} />
        </StudentInfoPageContent>
    );
}
