<script lang="ts">
  import { language } from '$lib/stores/language';
  import { locales } from '$lib/paraglide/runtime';
  import { messages } from '$lib/stores/messages';
  let availableLanguages = locales;

  function nextLanguage() {
    language.update(current => {
      const idx = availableLanguages.indexOf(current);
      const nextIdx = (idx + 1) % availableLanguages.length;
      return availableLanguages[nextIdx];
    });
  }
</script>

<button class="lang-switcher" on:click={nextLanguage} aria-label="Switch language">
  {$messages.lan()}
</button>

<style>
.lang-switcher {
  background: none;
  border: none;
  color: #007aff;
  font-size: 1rem;
  font-weight: 400;
  cursor: pointer;
  padding: 4px 12px;
  border-radius: 8px;
  transition: background 0.15s;
  font-family: -apple-system,BlinkMacSystemFont,sans-serif;
  outline: none;
  text-align: right;
}
.lang-switcher:active {
  background: rgba(229, 229, 234, 0.3);
}
</style> 