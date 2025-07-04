<script lang="ts">
  export let suggestions: { type: string; value: string; display: string; displayKannada?: string; }[] = [];
  export let search: string = '';
  export let onSelect: (s: any) => void = () => {};

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
    return '';
  }

  function highlightMatch(text: string, query: string) {
    if (!text || !query) return text;
    const idx = text.toLowerCase().indexOf(query.toLowerCase());
    if (idx === -1) return text;
    console.log([
      text.slice(0, idx),
      '<b>',
      text.slice(idx, idx + query.length),
      '</b>',
      text.slice(idx + query.length)
    ].join(''))
    return [
      text.slice(0, idx),
      '<b>',
      text.slice(idx, idx + query.length),
      '</b>',
      text.slice(idx + query.length)
    ].join('');
  }
</script>

{#if suggestions.length > 0}
  <div class="cupertino-suggestions-dropdown" role="listbox">
    {#each suggestions as s, i (s.type + '-' + (s.value ?? s.display ?? s.displayKannada ?? i))}
      <div
        class="cupertino-suggestion-item"
        role="option"
        aria-label={(s.displayKannada ? `${s.display}, ${s.displayKannada}` : s.display) }
        tabindex="0"
        on:click={() => onSelect(s)}
      >
        <span class="cupertino-suggestion-prefix">{getPrefix(s.type)}</span>
        <span class="cupertino-suggestion-labels">
          {#if search && s.display && s.display.toLowerCase().includes(search.trim().toLowerCase())}
            <span class="cupertino-suggestion-main">{@html highlightMatch(s.display, search)}</span>
            {#if s.displayKannada}
              <span class="cupertino-suggestion-secondary">{s.displayKannada}</span>
            {/if}
          {:else if search && s.displayKannada && s.displayKannada.toLowerCase().includes(search.trim().toLowerCase())}
            <span class="cupertino-suggestion-main">{@html highlightMatch(s.displayKannada, search)}</span>
            {#if s.display}
              <span class="cupertino-suggestion-secondary">{s.display}</span>
            {/if}
          {:else}
            {#if s.display}
              <span class="cupertino-suggestion-main">{s.display}</span>
            {/if}
            {#if s.displayKannada}
<!--              <span class="cupertino-suggestion-secondary">{s.displayKannada}</span>-->
            {/if}
          {/if}
        </span>
      </div>
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
  z-index: 20;
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