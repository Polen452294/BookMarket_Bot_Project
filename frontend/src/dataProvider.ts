import simpleRestProvider from "ra-data-simple-rest";
import { fetchUtils } from "react-admin";

/**
 * HTTP client для react-admin
 * Добавляет X-Bot-Admin-Token ко всем запросам
 */
const httpClient = (url: string, options: fetchUtils.Options = {}) => {
    if (!options.headers) {
        options.headers = new Headers({ Accept: "application/json" });
    }

    const token = import.meta.env.VITE_ADMIN_TOKEN;
    if (token) {
        (options.headers as Headers).set("X-Bot-Admin-Token", token);
    }

    return fetchUtils.fetchJson(url, options);
};

/**
 * ВАЖНО:
 * baseUrl указывает на /admin,
 * а Resource name = "orders"
 * → итоговый URL: /admin/orders
 */
const dataProvider = simpleRestProvider(
    "http://localhost:8000/admin",
    httpClient
);

export default dataProvider;
