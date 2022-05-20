import { getBestRedirect } from "./routes";

/**
 * Note: all tests here also test the one with a trailing slash (/) because I'm paranoid
 * about the asterisk matching it
 */

test("/students/states stays there", () => {
    expect(getBestRedirect("/editions/old/students/states", "new")).toEqual(
        "/editions/new/students/states"
    );
    expect(getBestRedirect("/editions/old/students/states/", "new")).toEqual(
        "/editions/new/students/states"
    );
});

test("/students stays there", () => {
    expect(getBestRedirect("/editions/old/students", "new")).toEqual("/editions/new/students");
    expect(getBestRedirect("/editions/old/students/", "new")).toEqual("/editions/new/students");
});

test("/students/:id goes to /students", () => {
    expect(getBestRedirect("/editions/old/students/id", "new")).toEqual("/editions/new/students");
});

test("/projects stays there", () => {
    expect(getBestRedirect("/editions/old/projects", "new")).toEqual("/editions/new/projects");
    expect(getBestRedirect("/editions/old/projects/", "new")).toEqual("/editions/new/projects");
});

test("/projects/:id goes to /projects", () => {
    expect(getBestRedirect("/editions/old/projects/id", "new")).toEqual("/editions/new/projects");
});

test("/users stays there", () => {
    expect(getBestRedirect("/editions/old/users", "new")).toEqual("/editions/new/users");
    expect(getBestRedirect("/editions/old/users/", "new")).toEqual("/editions/new/users");
});

test("/admins stays there", () => {
    expect(getBestRedirect("/admins", "new")).toEqual("/admins");
    expect(getBestRedirect("/admins/", "new")).toEqual("/admins");
});

test("/editions stays there", () => {
    expect(getBestRedirect("/editions", "new")).toEqual("/editions");
    expect(getBestRedirect("/editions/", "new")).toEqual("/editions");
});
