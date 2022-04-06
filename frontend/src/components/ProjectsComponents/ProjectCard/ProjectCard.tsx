import {
    CardContainer,
    CoachesContainer,
    CoachContainer,
    Delete,
    TitleContainer,
    Title,
    Client
} from "./styles";

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
                <Title>
                    {name}
                </Title>
                <Delete>X</Delete>
            </TitleContainer>

            <Client>{client}</Client>
            <CoachesContainer>
                {coaches.map((element, _index) => (
                    <CoachContainer key={_index}>{element}</CoachContainer>
                ))}
            </CoachesContainer>
        </CardContainer>
    );
}
