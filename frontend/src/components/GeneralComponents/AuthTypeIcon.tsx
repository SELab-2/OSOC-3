import { HiOutlineMail } from "react-icons/hi";
import { AiFillGithub, AiFillGoogleCircle, AiOutlineQuestionCircle } from "react-icons/ai";

/**
 * An icon representing the type of authentication
 * @param props.type email/github/google
 */
export default function AuthTypeIcon(props: { type: string }) {
    if (props.type === "email") {
        return <HiOutlineMail />;
    } else if (props.type === "github") {
        return <AiFillGithub />;
    } else if (props.type === "google") {
        return <AiFillGoogleCircle />;
    } else {
        return <AiOutlineQuestionCircle />;
    }
}
