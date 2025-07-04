import { writable } from 'svelte/store';

export const platforms = writable<any[]>([]);

export function setPlatforms(data: any[]) {
    platforms.set(data);
} 