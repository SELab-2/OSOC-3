import { useState } from "react";
import { Project, Partner } from "../../../data/interfaces";
import { Input, AddButton } from "./styles";

export default function PartnerInput({
    project,
    setProject,
}: {
    project: Project;
    setProject: (project: Project) => void;
}) {
    const [partner, setPartner] = useState("");

    return (
        <>
            <Input
                value={partner}
                onChange={e => {
                    setPartner(e.target.value);
                }}
                placeholder="Partner"
            />
            <AddButton
                onClick={() => {
                    addToPartners();
                }}
            >
                Add Partner
            </AddButton>
        </>
    );

    function addToPartners() {
        if (!project.partners.some(presentPartner => presentPartner.name === partner)) {
            const newPartner: Partner = { name: partner };
            const newPartners = [...project.partners];
            newPartners.push(newPartner);
            const newProject: Project = { ...project, partners: newPartners };
            setProject(newProject);
        }
        setPartner("");
    }
}
