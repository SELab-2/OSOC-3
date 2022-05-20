import { DragDropContext } from "react-beautiful-dnd";
import { StudentListFilters } from "../../components/StudentsComponents";

/**
 * @returns Page where admins and coaches can filter on students.
 */
function StudentsPage() {
    return (
        <DragDropContext onDragEnd={() => {}}>
            <StudentListFilters />
        </DragDropContext>
    );
}

export default StudentsPage;
