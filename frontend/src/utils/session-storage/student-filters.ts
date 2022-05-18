import { SessionStorageKey } from "../../data/enums";
import { DropdownRole } from "../../components/StudentsComponents/StudentListFilters/RolesFilter/RolesFilter";

export function getNameFilter(): string {
    const nameFilter = sessionStorage.getItem(SessionStorageKey.NAME_FILTER);
    return nameFilter === null ? "" : nameFilter;
}

export function getAlumniFilter(): boolean {
    const alumniFilter = sessionStorage.getItem(SessionStorageKey.ALUMNI_FILTER);
    return alumniFilter === null ? false : JSON.parse(alumniFilter);
}

export function getStudentCoachVolunteerFilter(): boolean {
    const studentCoachVolunteerFilter = sessionStorage.getItem(
        SessionStorageKey.STUDENT_COACH_VOLUNTEER_FILTER
    );
    return studentCoachVolunteerFilter === null ? false : JSON.parse(studentCoachVolunteerFilter);
}

export function getSuggestedFilter(): boolean {
    const suggestedFilter = sessionStorage.getItem(SessionStorageKey.SUGGESTED_FILTER);
    return suggestedFilter === null ? false : JSON.parse(suggestedFilter);
}

export function getRolesFilter(): DropdownRole[] {
    const rolesFilter = sessionStorage.getItem(SessionStorageKey.ROLES_FILTER);
    return rolesFilter === null ? [] : JSON.parse(rolesFilter);
}

export function setNameFilterStorage(nameFilter: string | null) {
    if (nameFilter === null) {
        sessionStorage.removeItem(SessionStorageKey.NAME_FILTER);
    } else {
        sessionStorage.setItem(SessionStorageKey.NAME_FILTER, nameFilter);
    }
}

export function setAlumniFilterStorage(alumniFilter: string | null) {
    if (alumniFilter === null) {
        sessionStorage.removeItem(SessionStorageKey.ALUMNI_FILTER);
    } else {
        sessionStorage.setItem(SessionStorageKey.ALUMNI_FILTER, alumniFilter);
    }
}

export function setStudentCoachVolunteerFilterStorage(studentCoachVolunteerFilter: string | null) {
    if (studentCoachVolunteerFilter === null) {
        sessionStorage.removeItem(SessionStorageKey.STUDENT_COACH_VOLUNTEER_FILTER);
    } else {
        sessionStorage.setItem(
            SessionStorageKey.STUDENT_COACH_VOLUNTEER_FILTER,
            studentCoachVolunteerFilter
        );
    }
}

export function setSuggestedFilterStorage(suggestedFilter: string | null) {
    if (suggestedFilter === null) {
        sessionStorage.removeItem(SessionStorageKey.SUGGESTED_FILTER);
    } else {
        sessionStorage.setItem(SessionStorageKey.SUGGESTED_FILTER, suggestedFilter);
    }
}

export function setRolesFilterStorage(rolesFilter: string | null) {
    if (rolesFilter === null) {
        sessionStorage.removeItem(SessionStorageKey.ROLES_FILTER);
    } else {
        sessionStorage.setItem(SessionStorageKey.ROLES_FILTER, rolesFilter);
    }
}
