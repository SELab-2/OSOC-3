import React, { useEffect, useState } from "react";
import { StudentListFilters } from "../../components/StudentsComponents";
import { getStudents } from "../../utils/api/students";

interface Student {
    name: string;
    amountOfSuggestions: number;
}

function StudentsPage() {
    const [students, setStudents] = useState<Student[]>([]);

    async function callGetStudents() {
        try {
            const response = await getStudents();
            setStudents(response);
        } catch (error) {
            console.log(error);
        }
    }

    useEffect(() => {
        callGetStudents();
    }, []);

    return (
        <div>
            <StudentListFilters students={students} />
        </div>
    );
}

export default StudentsPage;
