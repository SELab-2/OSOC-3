import React from "react";
import { StudentCard } from "../index";
import { StudentCardsList } from "./styles";

export default function StudentList() {
    return (
        <StudentCardsList>
            <StudentCard name="Riley Pacocha" />
            <StudentCard name="John Barks" />
            <StudentCard name="Tessa Hendrickx" />
            <StudentCard name="Some Indian guy with a really long name" />
            <StudentCard name="Some Indian guy with an even longer name than a really long name, damn man this name is so long it reminds me of something ;)" />
            <StudentCard name="john deere" />
            <StudentCard name="mac donalds" />
            <StudentCard name="Kentucky FC" />
            <StudentCard name="Quick fast" />
            <StudentCard name="Burger King" />
            <StudentCard name="Take Away" />
            <StudentCard name="Domino's Pieza" />
            <StudentCard name="Pizza Hutte" />
        </StudentCardsList>
    );
}
