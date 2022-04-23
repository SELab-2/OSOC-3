import { matchPath } from "react-router-dom";

/**
 * Get the best matching route to redirect to
 * Boils down to the most-specific route that can be used across editions
 */
export function getBestRedirect(location: string, editionName: string): string {
    // All /student/X routes should go to /students
    if (matchPath({ path: "/editions/:edition/students/*" }, location)) {
        return `/editions/${editionName}/students`;
    }

    // All /project/X routes should go to /projects
    if (matchPath({ path: "/editions/:edition/projects/*" }, location)) {
        return `/editions/${editionName}/projects`;
    }

    // /admins can stay where it is
    if (matchPath({ path: "/admins" }, location)) {
        return "/admins";
    }

    // All /users/X routes should go to /users
    if (matchPath({ path: "/editions/:edition/users/*" }, location)) {
        return `/editions/${editionName}/users`;
    }

    // Being on the edition-specific page should keep you there
    if (matchPath({ path: "/editions/:edition" }, location)) {
        return `/editions/${editionName}`;
    }

    // All the rest: go to /editions
    return "/editions";
}
