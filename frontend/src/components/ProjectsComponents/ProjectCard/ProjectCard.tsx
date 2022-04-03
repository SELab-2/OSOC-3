import { CardContainer, CoachesContainer, CoachContainer, Delete, TitleContainer } from "./styles";

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
            <TitleContainer>
                <div>
                    <h2>{name}</h2>
                </div>

                <Delete>X</Delete>
            </TitleContainer>

            <h3>{client}</h3>
            <CoachesContainer>
                {coaches.map((element, _index) => (
                    <CoachContainer key={_index}>{element}</CoachContainer>
                ))}
            </CoachesContainer>
        </CardContainer>
    );
}
