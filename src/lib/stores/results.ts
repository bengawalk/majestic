import { writable } from 'svelte/store';

export const results = writable<any[]>([]);

export function setResults(data: any[]) {
    results.set(data);
}
