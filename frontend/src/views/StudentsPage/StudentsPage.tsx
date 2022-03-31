import React from "react";
import { StudentCard } from "../../components/StudentsComponents";
import "./StudentsPage.css";

function Students() {
    const sidebar: boolean = true;
    return (
        <div>
            <div className={sidebar ? "side-menu active" : "side-menu"}>
                <input className="search-student" placeholder="search student" />
                <input className="roles-dropdown" placeholder="roles dropdown" />
                <p>Only Alumni</p>
                <p>Only students you've suggested for</p>
                <p>Only student coach volunteer</p>
                <p>Only available students</p>
                <button>Reset filters</button>
                <StudentCard />
                <StudentCard />
                <StudentCard />
                <StudentCard />
            </div>
        </div>
    );
}

export default Students;
