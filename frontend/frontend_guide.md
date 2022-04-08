# Frontend Guide

General guidelines & style conventions relating to frontend development. Don't do this, but do that!

A lot of these guidelines revolve around directory structure and cleaner components. We don't want `.tsx`-files with thousands of `classNames` scattered all over the place, but there are way better solutions as you'll see in this guide.

## Practical: Making API calls to the backend

There is a pre-defined `axiosInstance` for you to use, which has things like the base url pre-configured.

_Note that all logic should go to separate files, so the import path here suggests the file is in `/frontend/src/utils/api/`._

Don't do

```ts
import axios from "axios";

async function someApiCall() {
    await axios.get("https://sel2-3.ugent.be/api/students", headers={"Authorization": `Bearer ${token}`);
}
```

but do

```ts
import { axiosInstance } from "./api";

async function someApiCall() {
    // Note that we can now leave out the base url & headers!
    // Code is cleaner, shorter, and you can't make mistakes against the url anymore
    await axiosInstance.get("/students");
}
```

## Practical: TypeScript interfaces for API responses

In order to typehint the response of an API call, you can create an `interface`. This will tell TypeScript that certain fields are present, and what their type is, and it allows you to interact with the response as if it would be a class instance. Your IDE will also give intelligent code completion when using these interfaces.

**Interfaces that are only relevant to one file should be defined at the top of the file, interfaces relevant to multiple files should be moved to another directory**.

```ts
// /data/interfaces/students.ts

// This interface can probably be used in multiple places, so it should be in a publicly accessible file
export interface Student {
    id: Number;
    name: string;
    age: Number;
}
```

```ts
// /utils/api/students.ts

// This interface is specific to one API call, no need to expose it to other files
interface GetStudentsResponse {
    students: Student[]; // <- Yes, you can use interfaces as types in other interfaces
}

async function getStudents(): GetStudentsResponse {
    const response = await axiosInstance.get("/students");

    // The "as [interface]"-keyword will tell TypeScript that the response has the structure of [interface]
    return response as GetStudentsResponse;
}
```

### Note: you only have to add the fields that you care about

An interface can be seen as a "view" on an object, pulling some fields out. There's no need to create an interface for the entire API response body if you only need one field.

Of course, if an existing interface already has the field(s) you need, there's no need to make a smaller one just for the sake of leaving some fields out. This only applies to creating **new** interfaces for specific responses.

In the example below, `Student` has an `id`- and an `age`-field, but neither of them are used. There's no need to include them in the interface. If there would already be a `Student` interface, with **all** fields, you can use the existing interface instead of making a custom view.

Don't do

```ts
interface StudentResponse {
    id: Number; // <- Unused field
    name: string;
    age: Number; // <- Unused field
    // ...
}

async function getStudentName(id: Number): string {
    const student = (await axiosInstance.get(`/students/${id}`)) as StudentResponse;
    return student.name;
}
```

but do

```ts
interface StudentResponse {
    name: string; // <- Only field we use
}

async function getStudentName(id: Number): string {
    const student = (await axiosInstance.get(`/students/${id}`)) as StudentResponse;
    return student.name;
}
```

or, if an interface already exists, do

```ts
// "Student" already exists and has a lot of fields, "name" is one of those fields
// We don't care about the rest, but it's not necessary to make a new interface
// if the existing one can be used
// (it might even make the code more readable to use the old/generalized interface)
import { Student } from "../../data/interfaces/students";

async function getStudentName(id: Number): string {
    const student = (await axiosInstance.get(`/students/${id}`)) as Student;
    return student.name;
}
```

## Use `async-await` instead of `.then()`

The old way of handling asynchronous code used `function().then()`. The issue with this is that it becomes quite ugly very quickly, and also leads to the so-called "callback hell". The code executed _after_ the `.then()` **must** be placed inside of it, otherwise there are no guarantees about when or how it will execute. Further, you can't `return` from these callbacks, so things like returning the result of an API call are basically impossible (except for very ugly solutions like creating `Promise`-instances).

You should only use `.then()` when you really have no other choice. For example: when interacting with something that doesn't _allow_ `async function`s.

Don't do

```ts
function callbackHell(): Response {
    apiCall().then(response => {
        // How do you make "callbackHell()" return "response"?
        // "return" doesn't work here, as we are inside of a lambda
        otherApiCall().then(otherResponse => {
            // How do you make "callbackHell()" return "otherResponse"?
            // "return" doesn't work here either, as we are still inside of a lambda
        });
    });
}
```

but do

```ts
// Note the "async" keyword
async function asyncAwaitHeaven(): Promise<Response> {
    const response = await apiCall();
    const otherResponse = await otherApiCall(); // This line is only executed after the previous one is finished

    // You can now very easily return the response of the API call like you normally would
    return response;
}
```

Similarly, `.catch()` can be replaced by the `try-catch` pattern you're probably more familiar with.

Don't do

```ts
function thenCatch() {
    apiCall()
        .then(response => console.log(response))
        .catch(exception => console.log(exception));
}
```

but do

```ts
async function asyncCatch() {
    try {
        const response = await apiCall();
        console.log(response);
    } catch (exception) {
        console.log(exception);
    }
}
```

## Moving pages to separate directories

Don't do

```
views
	- LoginPage.tsx
	- HomePage.tsx
```

but do

```
views
    - LoginPage
    	- LoginPage.tsx
    - HomePage
    	- HomePage.tsx
```

## Keep `.css`-files next to the `.tsx`-files they are for

Don't do

```
css-files
	- App.css

views
	- App.tsx
```

but do

```
views
	- App
		- App.tsx
		- App.css
```

This keeps the directories clean, so we don't end up with a thousand `.css` files scattered throughout the repository. If a file is next to a component, you can instantly find one if you have the other.

## Use `react-bootstrap`-components instead of adding unnecessary Bootstrap `className`s

`react-bootstrap` has a lot of built-in components that do some basic & commonly-used functionality for you. It's cleaner to use these components than to make a `<div className={ "something" }/>` because it keeps the code more readable.

Don't do

```tsx
export default function Component() {
    return (
        <div className={"container"}>
            <div className={"button"}>{/* ... */}</div>
        </div>
    );
}
```

but do

```tsx
import Button from "react-bootstrap/Button";
import Container from "react-bootstrap/Container";

export default function Component() {
    return (
        <Container>
            <Button>{/* ... */}</Button>
        </Container>
    );
}
```

### Note: only import what you need

Docs on importing components can be found [here](https://react-bootstrap.github.io/getting-started/introduction/#importing-components).

Don't do

```tsx
// This pulls the entire library to only use this one component
import { Button } from "react-bootstrap";
```

but do

```tsx
// This navigates to the location of the component and only imports that
import Button from "react-bootstrap/Button";
```

More info & tutorials about `react-bootstrap`, including a list of all available components, can be found on their [website](https://react-bootstrap.github.io/getting-started/introduction/).

## Use `styled-components` instead of unnecessary `.css`-files, -classes, and inline styling

If you create a `.css`-class that you only apply to a single element (or a couple of elements in the same isolated component), it's better to create a `styled-component`. This keeps the `.tsx`-files clean, as there are no unnecessary `className`s on every element. It also makes the code a bit easier to read, as every component now has a name instead of being a `div`. The same goes for inline `style`-tags. **Don't do this**.

As you'll hopefully see in the example below, the resulting code is a lot calmer and less chaotic.

Only create `.css`-files if you really have to.

The name of this file should be `styles.ts`, and be present next to the `.tsx`-file it's for. If you would somehow end up with multiple `styles` in the same directory, prefix them with the name of the component (`Component.styles.ts`).

Don't do

```css
/* Component.css */
.page-content {
    color: red;
    background-color: blue;
}

/* ... */
```

```tsx
// Component.tsx
import "./Component.css"

export default function Component() {
    return (
        <div className={"page-content"} style={{ font-weight: "bold" }}>
        	{ /* ... More divs with a lot more classNames here */ }
    	</div>
    );
}
```

but do

```ts
// styles.ts
import styled from "styled-components";

// You can create a component for every tag there is,
// I'm just using a <div> in this example here.
// styled.h3`` also works just fine.
export const PageContent = styled.div`
    color: red;
    background-color: blue;
    font-weight: bold;
`;
```

```tsx
// Component.tsx
import { PageContent } from "./styles";

export default function Component() {
    // Notice how there are no classNames or inline styles, the code is a lot less hectic
    return <PageContent>{/* more styled-components here */}</PageContent>;
}
```

Directory structure:

```
components
	- SomePage
		- Component
			- Component.tsx
			- Component.css
			- styles.ts
```

### Note: you can also turn `react-bootstrap`-components into `styled-components` to keep the code even cleaner.

Combining the previous tip with this one. To create a `styled-component` from a `react-bootstrap`-component (or any other component you have made), by passing the component as an argument to the `styled`-function.

```ts
// styles.ts
import Container from "react-bootstrap/Container";
import styled from "styled-components";

export const BoldContainer = styled(Container)`
    font-weight: bold;
`;
```

More info & tutorials on `styled-components` can be found on their [website](https://styled-components.com/docs/basics).

## Split every page & component down into small components

We don't want massive `.tsx` files with hundreds of `<div>`s and 500 indents. Split every independent part down into small components that each have their own directory and isolated `.css` file.

Don't do

```
views
	- SomePage
		- SomePage.tsx
		- SomePage.css
```

```tsx
// SomePage.tsx
export default function SomePage() {
    return (
        <div>
            <div>// Page header, lots of code here</div>
            <div>// Page footer, also a lot of code here</div>
        </div>
    );
}
```

but do

```
components
	- SomePage			<- Components only related to this page should also go in a separate directory to split them from the rest
		- Header
			- Header.tsx
			- Header.css
			- styles.ts
		- Footer
			- Footer.tsx
			- Footer.css
			- styles.ts
views
	- SomePage
		- SomePage.tsx
		- SomePage.css
```

```tsx
// SomePage.tsx
export default function SomePage() {
    return (
        <div>
            <Header />
            <Footer />
        </div>
    );
}
```

```tsx
// Header.tsx
export default function Header() {
    return <div>{/* Either more small components here, or an acceptable amount of code */}</div>;
}
```

```tsx
// Footer.tsx
export default function Footer() {
    return <div>{/* Either more small components here, or an acceptable amount of code */}</div>;
}
```

## Use `index.ts`-files to re-export components and keep import paths short

In JavaScript (and, as a result, also TypeScript) `index.(j/t)s` can be used to export specific functions from a module, keeping the rest hidden.

If a piece of code isn't required outside of its module, don't export it in the `index.ts`-file. This way, only the "public" code is exported (and visible to outsider modules), while local logic is kept local.

You can create as many `index.ts`-files as you want, which can all re-export nested components, functions, `const` variables, and more. The only rule you should follow is that you shouldn't re-export something to a level where you don't need it anymore. If `/components/Header/Button` is only used in the `Header`, don't include it in the `index.ts`-file from `Header`. This would "include" it in the Header module, even though it's not used outside of it. Keep the component **private** to the module.

Don't do

```ts
// This import means "/Button/Button.ts", so we are mentioning Button twice
// even though it's obvious that that's what we're trying to import
import Button from "./Button/Button";
```

but do

```ts
// /Button/index.ts
export { default as Button } from "./Button";
```

```tsx
// The "/Button/index.ts"-file allows us to import from the name of the MODULE
// rather than going all the way to the ".ts(x)"-file
import { Button } from "./Button";
```

Directory structure:

```
components
	- Footer
		- Button
			- Button.tsx
			- index.ts      // Re-exports the Button: export { default as Button } from "./Button";
		- index.ts			// Re-exports the Footer: export { default as Footer } from "./Footer";
```

## Move logic to separate files

Just as we did in the backend, the main components don't need to handle the logic that they execute. They merely call functions defined elsewhere.

Don't do

```tsx
// Component.tsx
import { axiosInstance } from "../utils/api";

export default function Component() {
    return (
        // This makes the .tsx less readable
    	<Button onClick={() => axiosInstance.get("/students").then(...)}/>
    );
}
```

but do

```ts
// src/utils/api/students.ts
import { axiosInstance } from "./api";

export async function getStudents() {
    return await axiosInstance.get("/students");
}
```

```ts
// src/utils/api/index.ts
export { getStudents } from "./students";
```

```tsx
// Component.tsx
import { getStudents } from "../utils/api";

export default function Component() {
    return <Button onClick={getStudents} />;
}
```

## Don't add unnecessary lambdas

If a lambda expression does nothing but call another function (**without arguments**), then you might as well use that function.

`() => func()` is the exact same as `func`, but looks a lot more complex than it should be.

Don't do

```ts
<Button onClick={() => handleClick()} />
```

but do

```ts
<Button onClick={handleClick} />
```

This works for asynchronous functions too.

Don't do

```ts
<Button onClick={async () => handleClickAsync()} />
```

but do

```ts
<Button onClick={handleClickAsync} />
```
