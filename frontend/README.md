# Frontend

## Installing (and using) Yarn

*- What is my purpose?*

*- You install Yarn*

```bash
npm install --global yarn
```

:heavy_exclamation_mark: Do **not** use `npm` anymore! Yarn and npm shouldn't be used at the same time. 

```bash
# Installing new package
yarn add <package_name>

# Installing new package as a dev dependency
yarn add --dev <package_name>

# Installing all packages listed in package.json
yarn install
```

## Available Scripts

In the project directory, you can run:

### `yarn start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `yarn test`

Launches the test runner.

### `yarn build`

Builds the app for production to the `build` folder. It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.
