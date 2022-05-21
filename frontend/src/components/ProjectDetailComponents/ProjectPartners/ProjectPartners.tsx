import { TiDeleteOutline } from "react-icons/ti";
import { Project } from "../../../data/interfaces";
import PartnerInput from "../PartnerInput";

import { ClientContainer, Client, RemoveButton } from "./styles";

export default function ProjectPartners({
    project,
    editedProject,
    setEditedProject,
    editing,
}: {
    project: Project;
    editedProject: Project;
    setEditedProject: (project: Project) => void;
    editing: boolean;
}) {
    return (
        <>
            {editedProject.partners.map((element, _index) => (
                <ClientContainer key={_index}>
                    <Client>{element.name}</Client>
                    {editing && (
                        <RemoveButton
                            onClick={() => {
                                const newPartners = [...editedProject.partners];
                                newPartners.splice(_index, 1);
                                const newProject: Project = {
                                    ...project,
                                    partners: newPartners,
                                };
                                setEditedProject(newProject);
                            }}
                        >
                            <TiDeleteOutline size={"20px"} />
                        </RemoveButton>
                    )}
                </ClientContainer>
            ))}
            {editing && <PartnerInput project={editedProject!} setProject={setEditedProject} />}
        </>
    );
}
