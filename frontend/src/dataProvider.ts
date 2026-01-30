import simpleRestProvider from "ra-data-simple-rest";
import { fetchUtils } from "react-admin";

const API_URL = "http://localhost:8000/admin";

const httpClient = (url: string, options: fetchUtils.Options = {}) => {
  if (!options.headers) {
    options.headers = new Headers({ Accept: "application/json" });
  }

  const token = localStorage.getItem("admin_jwt");
  if (token) {
    (options.headers as Headers).set("Authorization", `Bearer ${token}`);
  }

  return fetchUtils.fetchJson(url, options);
};

const dataProvider = simpleRestProvider(API_URL, httpClient);
export default dataProvider;