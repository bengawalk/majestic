import { writable } from 'svelte/store';

export const routes = writable<any[]>([]);

export function setRoutes(data: any[]) {
    routes.set(data);
} 