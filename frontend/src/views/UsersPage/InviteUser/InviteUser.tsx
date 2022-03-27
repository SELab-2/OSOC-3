import React from "react";
import { getInviteLink } from "../../../utils/api/users";
import "./InviteUsers.css";
import { InviteInput, InviteButton, Loader, InviteContainer, Link, Error } from "./styles";

export default class InviteUser extends React.Component<
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
                this.setState({ link: ding, loading: false }); // TODO: fix email stuff
            });
        } else {
            this.setState({ valid: false, errorMessage: "Invalid email" });
        }
    }

    render() {
        let button;
        if (this.state.loading) {
            button = <Loader />;
        } else {
            button = (
                <div>
                    <InviteButton onClick={() => this.sendInvite()}>Send invite</InviteButton>
                </div>
            );
        }

        let error = null;
        if (this.state.errorMessage) {
            error = <Error>{this.state.errorMessage}</Error>;
        }

        let link = null;
        if (this.state.link) {
            link = <Link>{this.state.link}</Link>;
        }

        return (
            <div>
                <InviteContainer>
                    <InviteInput
                        className={this.state.valid ? "" : "email-field-error"}
                        placeholder="Invite user by email"
                        value={this.state.email}
                        onChange={e => this.setEmail(e.target.value)}
                    />
                    {button}
                </InviteContainer>
                {error}
                {link}
            </div>
        );
    }
}
