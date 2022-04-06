import {
    CardContainer,
    CoachesContainer,
    CoachContainer,
    NumberOfStudents,
    Delete,
    TitleContainer,
    Title,
    Client,
} from "./styles";

import { BsPersonFill } from "react-icons/bs";

export default function ProjectCard({
    name,
    client,
    numberOfStudents,
    coaches,
}: {
    name: string;
    client: string;
    numberOfStudents: number;
    coaches: string[];
}) {
    return (
        <CardContainer>
            <TitleContainer>
                <Title>{name}</Title>
                <Delete>X</Delete>
            </TitleContainer>

            <Client>
                {client}
                <NumberOfStudents>
                    {numberOfStudents}
                    <BsPersonFill />
                </NumberOfStudents>
            </Client>
            

            <CoachesContainer>
                {coaches.map((element, _index) => (
                    <CoachContainer key={_index}>{element}</CoachContainer>
                ))}
            </CoachesContainer>
        </CardContainer>
    );
}
