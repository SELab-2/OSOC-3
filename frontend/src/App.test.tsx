import React from "react";
import { shallow } from "enzyme";
import App from "./App";
import Router from "./Router";

test("app contains router", () => {
    const page = shallow(<App />);
    expect(page.find(Router).exists()).toBeTruthy();
});
