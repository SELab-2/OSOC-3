import { CardContainer, CoachesContainer, CoachContainer, Delete } from "./styles";

export default function ProjectCard({
    name,
    client,
    coaches,
}: {
    name: string;
    client: string;
    coaches: string[];
}) {
    return (
        <CardContainer>
            <h2>{name}</h2>
            <h3>{client}</h3>
            <CoachesContainer>
                {coaches.map((element, index) => (
                    <CoachContainer>{element}</CoachContainer>
                ))}
            </CoachesContainer>
            <Delete>X</Delete>
        </CardContainer>
    );
}
