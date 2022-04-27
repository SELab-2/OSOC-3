import { AuthTypeDiv, EmailAndAuthDiv, EmailDiv } from "./styles";
import AuthTypeIcon from "./AuthTypeIcon";
import { User } from "../../utils/api/users/users";

/**
 * Email adress + auth type icon of a given user.
 * @param props.user The given user.
 */
export default function EmailAndAuth(props: { user: User | undefined }) {
    if (props.user === undefined) {
        return null;
    }
    return (
        <EmailAndAuthDiv>
            <AuthTypeDiv>
                <AuthTypeIcon type={props.user.auth.authType} />
            </AuthTypeDiv>
            <EmailDiv>{props.user.auth.email}</EmailDiv>
        </EmailAndAuthDiv>
    );
}
