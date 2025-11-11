//feature-scoped API calls (uses services/http)
// used for the server calls in creating routes


import { http } from "@/services/http.js";

export const startServer = (id) =>
  http.post(`/api/servers/${id}/start`, {});

export const stopServer = (id) =>
  http.post(`/api/servers/${id}/stop`, {});

export const deleteServer = (id) =>
  http.del(`/api/servers/${id}`);