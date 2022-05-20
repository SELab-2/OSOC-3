import { DragDropContext } from "react-beautiful-dnd";
import { StudentListFilters } from "../../components/StudentsComponents";

/**
 * @returns Page where admins and coaches can filter on students.
 */
function StudentsPage() {
    return (
        <DragDropContext onDragEnd={result => console.log(result)}>
            <StudentListFilters />
        </DragDropContext>
    );
}

export default StudentsPage;
