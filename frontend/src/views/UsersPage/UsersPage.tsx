import React from "react";
import "./UsersPage.css";
import { getInviteLink } from "../../utils/api/users";

class InviteUser extends React.Component<
    {},
    {
        email: string;
        valid: boolean;
        errorMessage: string | null;
        loading: boolean;
        link: string | null;
    }
> {
    constructor(props = {}) {
        super(props);
        this.state = { email: "", valid: true, errorMessage: null, loading: false, link: null };
    }

    setEmail(email: string) {
        this.setState({ email: email, valid: true, link: null, errorMessage: null });
    }

    async sendInvite() {
        if (/[^@\s]+@[^@\s]+\.[^@\s]+/.test(this.state.email)) {
            this.setState({ loading: true });
            getInviteLink("edition", this.state.email).then(ding => {
                this.setState({ link: ding, loading: false });
            });
        } else {
            this.setState({ valid: false, errorMessage: "Invalid email" });
        }
    }

    render() {
        let button;
        if (this.state.loading) {
            button = <div className="loader" />;
        } else {
            button = (
                <div>
                    <button onClick={() => this.sendInvite()}>Send invite</button>
                </div>
            );
        }
        let error = null;
        if (this.state.errorMessage) {
            error = <div className="error">{this.state.errorMessage}</div>;
        }
        let link = null;
        if (this.state.link) {
            link = <div className="link">{this.state.link}</div>;
        }
        return (
            <div>
                <div className="invite-user-container">
                    <input
                        id="email-field"
                        className={this.state.valid ? "" : "email-field-error"}
                        type="email"
                        name="email"
                        placeholder="Invite user by email"
                        value={this.state.email}
                        onChange={e => this.setEmail(e.target.value)}
                    />
                    {button}
                </div>
                {error}
                {link}
            </div>
        );
    }
}

function UsersPage() {
    return <InviteUser />;
}

export default UsersPage;
