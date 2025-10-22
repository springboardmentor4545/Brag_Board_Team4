// API base URL
export const API_BASE_URL = "http://localhost:8000";

// API endpoints
export const API_ENDPOINTS = {
  USERS: {
    REGISTER: "/users",
    LOGIN: "/users/login",
    ME: "/users/me",
  },
  ITEMS: {
    LIST: "/items",
    CREATE: "/items",
    GET: (id) => `/items/${id}`,
    UPDATE: (id) => `/items/${id}`,
    DELETE: (id) => `/items/${id}`,
  },
  COMMENTS: {
    LIST: (itemId) => `/items/${itemId}/comments`,
    CREATE: (itemId) => `/items/${itemId}/comments`,
  },
  REACTIONS: {
    LIST: (itemId) => `/items/${itemId}/reactions`,
    CREATE: (itemId) => `/items/${itemId}/reactions`,
  },
  ADMIN: {
    DELETE_ITEM: (id) => `/admin/items/${id}`,
    DEACTIVATE_USER: (id) => `/admin/users/${id}/deactivate`,
  },
};
