import { HiOutlineMail } from "react-icons/hi";
import { AiFillGithub, AiOutlineQuestionCircle } from "react-icons/ai";
import { AuthType } from "../../../data/enums";

/**
 * An icon representing the type of authentication
 */
export default function AuthTypeIcon(props: { type: AuthType }) {
    switch (props.type) {
        case AuthType.Email:
            return <HiOutlineMail />;
        case AuthType.GitHub:
            return <AiFillGithub />;
    }
    return <AiOutlineQuestionCircle />;
}
