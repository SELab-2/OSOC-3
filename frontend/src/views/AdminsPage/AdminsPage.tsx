import React, { useCallback, useEffect, useState } from "react";
import { AdminsContainer } from "./styles";
import { getAdmins } from "../../utils/api/users/admins";
import { AddAdmin, AdminList } from "../../components/AdminsComponents";
import { User } from "../../utils/api/users/users";
import { SearchBar } from "../../components/Common/Forms";
import { Error, SearchFieldDiv, TableDiv } from "../../components/Common/Users/styles";
import LoadSpinner from "../../components/Common/LoadSpinner";

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
            list = <LoadSpinner show={true} />;
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
            <SearchFieldDiv>
                <SearchBar
                    onChange={e => filter(e.target.value)}
                    value={searchTerm}
                    placeholder="Search name..."
                />
            </SearchFieldDiv>
            <AddAdmin adminAdded={addAdmin} />
            <TableDiv>{list}</TableDiv>
        </AdminsContainer>
    );
}
