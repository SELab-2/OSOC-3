import { HiOutlineMail } from "react-icons/hi";
import { AiFillGithub, AiFillGoogleCircle, AiOutlineQuestionCircle } from "react-icons/ai";
import { AuthType } from "../../utils/api/users/users";

/**
 * An icon representing the type of authentication
 */
export default function AuthTypeIcon(props: { type: AuthType }) {
    switch (props.type) {
        case AuthType.Email:
            return <HiOutlineMail />;
        case AuthType.GitHub:
            return <AiFillGithub />;
        case AuthType.Google:
            return <AiFillGoogleCircle />;
    }
    return <AiOutlineQuestionCircle />;
}
