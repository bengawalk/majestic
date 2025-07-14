import { writable } from 'svelte/store';
import { setLocale, locales } from '$lib/paraglide/runtime';

export type AvailableLanguageTag = typeof locales[number];

const getInitialLanguage = (): AvailableLanguageTag => {
  if (typeof window !== 'undefined') {
    const saved = localStorage.getItem('app_language');
    if (saved && (locales as readonly string[]).includes(saved)) return saved as AvailableLanguageTag;
  }
  return 'en';
};
const initialTag = getInitialLanguage();
setLocale(initialTag);
export const language = writable<AvailableLanguageTag>(initialTag);

if (typeof window !== 'undefined') {
  language.subscribe((value) => {
    localStorage.setItem('app_language', value);
    setLocale(value, { reload: false }); // This will update Paraglide's locale
  });
} 