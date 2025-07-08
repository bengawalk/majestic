import { derived } from 'svelte/store';
import { language } from './language';
import * as m from '$lib/paraglide/messages';

export const messages = derived(language, () => m); 