import { writable } from 'svelte/store';

export const areas = writable<any[]>([]);

export function setAreas(data: any[]) {
    areas.set(data);
}
