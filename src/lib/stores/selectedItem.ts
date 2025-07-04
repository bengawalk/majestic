import { writable } from 'svelte/store';

export const selectedItem = writable<any>(undefined);
export const previousSelectedItem = writable<any>(undefined); 