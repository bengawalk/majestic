<script lang="ts">
  import {search} from "$lib/stores/search";
  import {previousSelectedItem, selectedItem} from "$lib/stores/selectedItem";

  export let suggestions: { type: string; value: string; display: string; displayKannada?: string; }[] = [];
  export let onSelect: (s: any) => void = (s) => {
    previousSelectedItem.set(undefined);
    selectedItem.set(undefined);
    selectedItem.set(s);
  };

  // Expose a method to select the first suggestion
  export function selectFirst() {
    if (suggestions.length > 0) {
      onSelect(suggestions[0]);
    }
  }

  function getPrefix(type: string) {
    if (type === 'Area' || type === 'Via') return '+';
    if (type === 'Stop') return '-';
    if (type === 'Route') return '=';
    if (type === 'Platform') return '#';
    return '';
  }

  function highlightSegments(text: string, query: string) {
    if (!text || !query) return [{ text, highlight: false }];
    const idx = text.toLowerCase().indexOf(query.toLowerCase());
    if (idx === -1) return [{ text, highlight: false }];
    return [
      { text: text.slice(0, idx), highlight: false },
      { text: text.slice(idx, idx + query.length), highlight: true },
      { text: text.slice(idx + query.length), highlight: false }
    ];
  }
</script>

{#if suggestions.length > 0}
  <div class="cupertino-suggestions-dropdown" role="listbox">
    {#each suggestions as s, i (s.type + '-' + (s.value ?? s.display ?? s.displayKannada ?? i))}
      <button
        type="button"
        class="cupertino-suggestion-item"
        role="option"
        aria-label={(s.displayKannada ? `${s.display}, ${s.displayKannada}` : s.display) }
        on:click={() => onSelect(s)}
      >
        <span class="cupertino-suggestion-prefix">{getPrefix(s.type)}</span>
        <span class="cupertino-suggestion-labels">
          {#if $search && s.display && s.display.toLowerCase().includes($search.trim().toLowerCase())}
            <span class="cupertino-suggestion-main">
              {#each highlightSegments(s.display, $search) as seg}
                {#if seg.highlight}<b>{seg.text}</b>{:else}{seg.text}{/if}
              {/each}
            </span>
            {#if s.displayKannada}
              <span class="cupertino-suggestion-secondary">{s.displayKannada}</span>
            {/if}
          {:else if $search && s.displayKannada && s.displayKannada.toLowerCase().includes($search.trim().toLowerCase())}
            <span class="cupertino-suggestion-main">
              {#each highlightSegments(s.displayKannada, $search) as seg}
                {#if seg.highlight}<b>{seg.text}</b>{:else}{seg.text}{/if}
              {/each}
            </span>
            {#if s.display}
              <span class="cupertino-suggestion-secondary">{s.display}</span>
            {/if}
          {:else}
            {#if s.display}
              <span class="cupertino-suggestion-main">{s.display}</span>
            {/if}
            {#if s.displayKannada}
              <span class="cupertino-suggestion-secondary">{s.displayKannada}</span>
            {/if}
          {/if}
        </span>
      </button>
    {/each}
  </div>
{/if}

<style>
.cupertino-suggestions-dropdown {
  position: absolute;
  left: 0;
  right: 0;
  top: 100%;
  margin-top: 4px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 16px 0 rgba(60,60,67,0.10);
  z-index: 200;
  padding: 8px 0;
  max-height: 260px;
  overflow-y: auto;
  font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;
}
.cupertino-suggestion-item {
  padding: 14px 20px 14px 20px;
  font-size: 16px;
  color: #222;
  cursor: pointer;
  transition: background 0.15s;
  display: flex;
  align-items: flex-start;
  gap: 8px;
  min-height: 48px;
  flex-direction: row;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
}
.cupertino-suggestion-item:hover, .cupertino-suggestion-item:focus {
  background: #f1f1f3;
  outline: none;
}
.cupertino-suggestion-prefix {
  font-size: 18px;
  font-weight: 700;
  color: #888;
  flex-shrink: 0;
  margin-right: 2px;
  margin-top: 1px;
}
.cupertino-suggestion-main {
  font-size: 17px;
  margin-top: 2px;
  color: #222;
  font-weight: 400;
  display: block;
  line-height: 1.2;
}
.cupertino-suggestion-main b {
  font-weight: 700;
}
.cupertino-suggestion-secondary {
  display: block;
  font-size: 14px;
  color: #888;
  margin-top: 2px;
  line-height: 1.1;
}
.cupertino-suggestion-labels {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
}
</style> 