import axios from "axios";
import { axiosInstance } from "./api";

export async function getProjects(edition: string) {
    try {
        const response = await axiosInstance.get("/editions/" + edition + "/projects");
        console.log(response);
        
        const projects = response.data;
        return projects;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            return false;
        } else {
            throw error;
        }
    }
}
