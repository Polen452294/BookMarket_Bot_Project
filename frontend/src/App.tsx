import { Admin, Resource } from "react-admin";
import dataProvider from "./dataProvider";
import { authProvider } from "./authProvider";
import OrdersList from "./resources/orders";

export default function App() {
  return (
    <Admin dataProvider={dataProvider} authProvider={authProvider}>
      <Resource name="orders" list={OrdersList} />
    </Admin>
  );
}