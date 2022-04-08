import { useParams } from "react-router-dom";

export default function ProjectDetailPage() {
    const params = useParams();
    const projectId = params.projectId;

    return <div>{projectId}</div>;
}
