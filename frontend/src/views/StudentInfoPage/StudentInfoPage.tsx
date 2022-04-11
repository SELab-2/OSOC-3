import React, { useEffect, useState } from "react";
import "./StudentInfoPage.css";
import { StudentListFilters } from "../../components/StudentsComponents";
import { getStudents } from "../../utils/api/students";

interface Student {
    name: string;
    amountOfSuggestions: number;
}

function StudentInfoPage() {
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
        <div className="student-info-page">
            <StudentListFilters students={students} />
            <button className="remove-student">Remove Student</button>
            <div className="student-information">
                <div className="fullname">
                    <h1 className="firstname">Riley</h1>
                    <h1 className="lastname">Pacocha</h1>
                </div>
                <p className="prefered-name">Prefered name: "Rey"</p>
                <div className="line-break"></div>
                <h4 className="student-information-section">Suggestions</h4>
                <p>Wow this student is really incredible! We should give her a project!</p>
                <p>Wow this student is really incredible! We should give her a project!</p>
                <p>Wow this student is really incredible! We should give her a project!</p>
                <div className="line-break"></div>
                <h4 className="student-information-section">Personal information</h4>
                <p className="email-field">
                    Email <p>riley.pacocha@test.com</p>
                </p>
                <p className="phonenumber-field">
                    Phone number <p>0123 456 789</p>
                </p>
                <p className="alumni-field">
                    Is an alumni? <p>Yes</p>
                </p>
                <p className="studentcoach-field">
                    Wants to be student coach? <p>Yes</p>
                </p>
                <div className="line-break"></div>
                <h4 className="student-information-section">Skills</h4>
                <div className="roles-field">
                    Roles:
                    <div className="roles-in-roles-field">
                        <li>Frontend</li>
                        <li>Design</li>
                        <li>Communication</li>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default StudentInfoPage;
