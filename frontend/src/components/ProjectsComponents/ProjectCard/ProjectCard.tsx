import {
    CardContainer,
    CoachesContainer,
    CoachContainer,
    CoachText,
    NumberOfStudents,
    Delete,
    TitleContainer,
    Title,
    ClientContainer,
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
            <ClientContainer>
                <Client>{client}</Client>
                <NumberOfStudents>
                    {numberOfStudents}
                    <BsPersonFill />
                </NumberOfStudents>
            </ClientContainer>

            <CoachesContainer>
                {coaches.map((element, _index) => (
                    <CoachContainer key={_index}>
                        <CoachText>{element}</CoachText>
                    </CoachContainer>
                ))}
            </CoachesContainer>
        </CardContainer>
    );
}
