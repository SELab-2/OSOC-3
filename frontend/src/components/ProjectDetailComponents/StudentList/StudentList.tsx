import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Student } from "../../../data/interfaces/students";
import { getStudents } from "../../../utils/api/students";
import { StudentContainer, StudentListContainer } from "./styles";
import { Draggable, Droppable } from "react-beautiful-dnd";

export default function StudentList() {
    const [students, setStudents] = useState<Student[]>([]);
    const [gotStudents, setGotStudents] = useState(false);

    const params = useParams();
    const editionId = params.editionId!;

    useEffect(() => {
        async function callStudents(newPage: number) {
            const response = await getStudents(editionId, "", [], false, false, 0);

            if (response) {
                setGotStudents(true);
                setStudents(response.students);
            }
        }
        if (!gotStudents) callStudents(0);
    }, [editionId, gotStudents, students]);

    return (
        <StudentListContainer>
            <Droppable droppableId="students" isDropDisabled={true}>
                {(provided, snapshot) => (
                    <div ref={provided.innerRef} {...provided.droppableProps}>
                        {students.map((student, index) => (
                            <Draggable draggableId={student.studentId.toString()} index={index} key={index}>
                                {(provided, snapshot) => (
                                    <StudentContainer
                                        key={student.studentId}
                                        ref={provided.innerRef}
                                        {...provided.draggableProps}
                                        {...provided.dragHandleProps}
                                    >
                                        {student.firstName}
                                        <br></br>
                                        {student.lastName}
                                    </StudentContainer>
                                )}
                            </Draggable>
                        ))}
                        {provided.placeholder}
                    </div>
                )}
            </Droppable>
        </StudentListContainer>
    );
}
