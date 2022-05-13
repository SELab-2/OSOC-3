import { User } from "../../utils/api/users/users";
import { DropdownEmailDiv, NameDiv } from "./styles";
import EmailAndAuth from "./EmailAndAuth";

/**
 * An item from a dropdown menu containing a user's name and email.
 * @param props.user The user which is represented.
 */
export default function UserMenuItem(props: { user: User }) {
    return (
        <div>
            <NameDiv>{props.user.name}</NameDiv>
            <DropdownEmailDiv>
                <EmailAndAuth user={props.user} />
            </DropdownEmailDiv>
        </div>
    );
}
