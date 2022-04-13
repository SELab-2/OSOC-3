import React, { useEffect, useState } from "react";
import { AdminsContainer } from "./styles";
import { getAdmins } from "../../utils/api/users/admins";
import { Error, SpinnerContainer } from "../../components/UsersComponents/Requests/styles";
import { AddAdmin, AdminList } from "../../components/AdminsComponents";
import { Spinner } from "react-bootstrap";
import { User } from "../../utils/api/users/users";
import { SearchInput } from "../../components/styles";

export default function AdminsPage() {
    const [admins, setAdmins] = useState<User[]>([]);
    const [gettingData, setGettingData] = useState(false);
    const [searchTerm, setSearchTerm] = useState("");
    const [gotData, setGotData] = useState(false);
    const [error, setError] = useState("");
    const [moreAdminsAvailable, setMoreAdminsAvailable] = useState(true);

    async function getData(page: number, filter: string | undefined = undefined) {
        if (filter === undefined) {
            filter = searchTerm;
        }
        setGettingData(true);
        setError("");
        try {
            const response = await getAdmins(page, filter);
            if (response.users.length !== 25) {
                setMoreAdminsAvailable(false);
            }
            if (page === 0) {
                setAdmins(response.users);
            } else {
                setAdmins(admins.concat(response.users));
            }

            setGotData(true);
            setGettingData(false);
        } catch (exception) {
            setError("Oops, something went wrong...");
            setGettingData(false);
        }
    }

    useEffect(() => {
        if (!gotData && !gettingData && !error) {
            getData(0);
        }
    });

    function filter(word: string) {
        setGotData(false);
        setSearchTerm(word);
        setAdmins([]);
        setMoreAdminsAvailable(true);
        getData(0, word);
    }

    function adminAdded(user: User) {
        if (user.name.includes(searchTerm)) {
            setAdmins([user].concat(admins));
        }
    }

    let list;
    if (admins.length === 0) {
        if (gettingData) {
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
                loading={gettingData}
                gotData={gotData}
                refresh={() => getData(0)}
                getMoreAdmins={getData}
                moreAdminsAvailable={moreAdminsAvailable}
            />
        );
    }

    return (
        <AdminsContainer>
            <SearchInput value={searchTerm} onChange={e => filter(e.target.value)} />
            <AddAdmin adminAdded={adminAdded} />
            {list}
            <Error> {error} </Error>
        </AdminsContainer>
    );
}
