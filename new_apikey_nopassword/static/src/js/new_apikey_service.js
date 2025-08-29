/** @odoo-module **/

import { registry } from "@web/core/registry";

const newApikeyService = {
    dependencies: [],
    start(env, deps) {
        console.log("hello javascript from new_apikey_nopassword");
        // A service must return an object
        return {
            message: "Service started successfully!",
        };
    },
};

registry.category("services").add("newApikeyService", newApikeyService);
