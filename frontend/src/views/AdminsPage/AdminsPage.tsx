import React, { useCallback, useEffect, useState } from "react";
import { AdminsContainer } from "./styles";
import { getAdmins } from "../../utils/api/users/admins";
import { Error, SpinnerContainer } from "../../components/UsersComponents/Requests/styles";
import { AddAdmin, AdminList } from "../../components/AdminsComponents";
import { Spinner } from "react-bootstrap";
import { User } from "../../utils/api/users/users";
import { SearchInput } from "../../components/styles";

export default function AdminsPage() {
    const [allAdmins, setAllAdmins] = useState<User[]>([]);
    const [admins, setAdmins] = useState<User[]>([]);
    const [loading, setLoading] = useState(false);
    const [searchTerm, setSearchTerm] = useState("");
    const [gotData, setGotData] = useState(false);
    const [error, setError] = useState("");

    const getData = useCallback(async () => {
        setError("");
        try {
            let adminsAvailable = true;
            let page = 0;
            let newAdmins: User[] = [];
            while (adminsAvailable) {
                const response = await getAdmins(page, searchTerm);
                if (page === 0) {
                    newAdmins = response.users;
                } else {
                    newAdmins = newAdmins.concat(response.users);
                }
                adminsAvailable = response.users.length !== 0;
                page += 1;
            }
            setGotData(true);
            setAdmins(newAdmins);
            setAllAdmins(newAdmins);
        } catch (exception) {
            setError("Oops, something went wrong...");
        }
        setLoading(false);
    }, [searchTerm]);

    useEffect(() => {
        if (!gotData && !loading && !error) {
            setLoading(true);
            getData();
        }
    }, [gotData, loading, error, getData]);

    function addAdmin(user: User) {
        setAllAdmins(allAdmins.concat([user]));
        if (user.name.includes(searchTerm)) {
            setAdmins([user].concat(admins));
        }
    }

    function removeAdmin(user: User) {
        setAllAdmins(allAdmins.filter(el => el !== user));
        setAdmins(admins.filter(el => el !== user));
    }

    function filter(searchTerm: string) {
        setSearchTerm(searchTerm);
        const newAdmins: User[] = [];
        for (const admin of allAdmins) {
            if (admin.name.toUpperCase().includes(searchTerm.toUpperCase())) {
                newAdmins.push(admin);
            }
        }
        setAdmins(newAdmins);
    }

    let list;
    if (admins.length === 0) {
        if (loading) {
            list = (
                <SpinnerContainer>
                    <Spinner animation="border" />
                </SpinnerContainer>
            );
        } else if (gotData) {
            list = <div>No admins found</div>;
        } else {
            list = <Error>{error}</Error>;
        }
    } else {
        list = (
            <AdminList
                admins={admins}
                loading={loading}
                gotData={gotData}
                removeAdmin={removeAdmin}
            />
        );
    }

    return (
        <AdminsContainer>
            <SearchInput
                value={searchTerm}
                onChange={e => {
                    filter(e.target.value);
                }}
            />
            <AddAdmin adminAdded={addAdmin} />
            {list}
        </AdminsContainer>
    );
}
