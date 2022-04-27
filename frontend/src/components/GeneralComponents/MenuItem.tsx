import { User } from "../../utils/api/users/users";
import { EmailDiv, NameDiv } from "./styles";
import EmailAndAuth from "./EmailAndAuth";

/**
 * An item from a dropdown menu containing a user's name and email.
 * @param props.user The user which is represented.
 */
export default function UserMenuItem(props: { user: User }) {
    return (
        <div>
            <NameDiv>{props.user.name}</NameDiv>
            <EmailDiv>
                <EmailAndAuth user={props.user} />
            </EmailDiv>
        </div>
    );
}
