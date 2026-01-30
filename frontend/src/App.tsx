import { Admin, Resource } from "react-admin";
import dataProvider from "./dataProvider";

import OrdersList from "./resources/orders";

export default function App() {
    return (
        <Admin dataProvider={dataProvider}>
            <Resource name="orders" list={OrdersList} />
        </Admin>
    );
}
