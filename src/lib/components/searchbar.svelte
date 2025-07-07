<script lang="ts">
  import { routes } from '$lib/stores/routes';
  import { setResults } from '$lib/stores/results';
  import { get } from 'svelte/store';
  import {createEventDispatcher, onMount, tick} from 'svelte';
  import Dropdown from './dropdown.svelte';
  import { search } from '$lib/stores/search';
  import {previousSelectedItem} from "$lib/stores/selectedItem";

  export let searchFocused: boolean;
  export let searchInput: HTMLInputElement | null = null;
  export let voiceSearchActive: boolean = false;
  export let selectedItem: any = null;
  export let showBackButton: boolean = false;

  let speechSupported = false;
  let recognizing = false;
  let recognition: SpeechRecognition | null = null;

  const dispatch = createEventDispatcher();

  // Dropdown suggestions
  let suggestions: { type: string; value: string; display: string; displayKannada?: string; }[] = [];
  let dropdownRef;

  onMount(() => {
    speechSupported = 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window;
    if (speechSupported) {
      const SpeechRecognitionClass = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition;
      recognition = new SpeechRecognitionClass();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'en-IN';
      recognition.onstart = () => voiceSearchActive = true;
      recognition.onresult = (event: any) => {
        if (event.results && event.results[0] && event.results[0][0]) {
          search.set(event.results[0][0].transcript);
          setTimeout(() => {
            if (dropdownRef && typeof dropdownRef.selectFirst === 'function') {
              dropdownRef.selectFirst();
            }
          }, 0);
        }
        recognizing = false;
        voiceSearchActive = false;
      };
      recognition.onend = () => {
        recognizing = false;
        voiceSearchActive = false;
      };
      recognition.onerror = () => {
        recognizing = false;
        voiceSearchActive = false;
      };
    }
  });

  function startVoiceSearch() {
    if (recognition && !recognizing) {
      recognizing = true;
      recognition.start();
    } else if (recognition && recognizing) {
      recognition.stop();
      recognizing = false;
      voiceSearchActive = false;
    }
  }

  function clearSearch() {
    search.set('');
    selectedItem.set(undefined);
    previousSelectedItem.set(undefined);
    searchInput?.focus();
  }

  function handleBack() {
    selectedItem.set(undefined);
    previousSelectedItem.set(undefined);
    search.set('');
    searchFocused = false;
    voiceSearchActive = false;
    setResults(get(routes));
    dispatch('back');
    dispatch('closeSheet');
    searchInput?.blur();
  }

  function handleSelectSuggestion(s) {
    selectedItem.set(undefined);
    previousSelectedItem.set(undefined);
    tick().then( () => {
      search.set(s.display);
      searchFocused = false;
      voiceSearchActive = false;
      dispatch('select', s);
    });
  }

  // Search logic: by destination or bus number (not platform)
  $: if ($search && $search.trim().length > 0) {
    const q = $search.trim().toLowerCase();
    const allRoutes = get(routes);
    const matched = new Set();
    // Update results for map
    // const matched = allRoutes.filter(item => {
    //   return Object.entries(item).some(([key, value]) => {
    //     if (key === "platform") return false;
    //     if (Array.isArray(value)) {
    //       return value.some(v => v.name?.toLowerCase().includes(q) || v.nameKannada?.toLowerCase().includes(q));
    //     }
    //     return String(value).toLowerCase().includes(q);
    //   });
    // });
    // setResults(matched);
    const areaViaSet = new Map<string, {type: string, display: string, displayKannada: string, value: string}>();
    const stopSet = new Map<string, {display: string, displayKannada: string, value: string}>();
    const routeSet = new Map<string, {display: string, value: string}>();
    // const platformSet = new Map<string, {type: string, display: string, value: string}>
    for (const route of allRoutes) {
      // if (route.platformNumber)
        // if (route.platformNumber.toLowerCase().includes(q)) {
        //   platformSet.set(route.platformNumber, {type: 'Platform', display: `Platform ${route.platformNumber}`, value: route.platformNumber});
        //   matched.add(route);
        // }
      // Area
      if (route.area) {
        if (
          (route.area.name && route.area.name.toLowerCase().includes(q)) ||
          (route.area.nameKannada && route.area.nameKannada.toLowerCase().includes(q))
        ) {
          if (route.area.name) {
            areaViaSet.set(route.area.name, {type: 'Area', display: route.area.name, displayKannada: route.area.nameKannada || '', value: route.area.name});
            matched.add(route);
          }
        }
      }
      // Via (handle both array and object)
      if (route.via) {
        if (Array.isArray(route.via)) {
          for (const v of route.via) {
            if (
              (v.name && v.name.toLowerCase().includes(q)) ||
              (v.nameKannada && v.nameKannada.toLowerCase().includes(q))
            ) {
              if (v.name) {
                areaViaSet.set(v.name, {type: 'Area', display: v.name, displayKannada: v.nameKannada || '', value: v.name});
                matched.add(route);
              }
            }
          }
        } else if (
          (route.via.name && route.via.name.toLowerCase().includes(q)) ||
          (route.via.nameKannada && route.via.nameKannada.toLowerCase().includes(q))
        ) {
          if (route.via.name) {
            areaViaSet.set(route.via.name, {type: 'Area', display: route.via.name, displayKannada: route.via.nameKannada || '', value: route.via.name});
            matched.add(route);
          }
        }
      }
      // Stops
      if (route.stops && Array.isArray(route.stops)) {
        for (const s of route.stops) {
          if(s.name && s.name == "Kempegowda Bus Station" || s.name == "Kempegowda Bus Stand") {
            continue;
          }
          if (
            (s.name && s.name.toLowerCase().includes(q)) ||
            (s.nameKannada && s.nameKannada.toLowerCase().includes(q))
          ) {
            if (s.name) {
              stopSet.set(s.name, {display: s.name, displayKannada: s.nameKannada || '', value: s.name});
              matched.add(route);
            }
          }
        }
      }
      // Route number
      if (route.number && route.number.toLowerCase().includes(q)) {
        if (route.number) {
          routeSet.set(route.number, {display: route.number, value: route.number});
          matched.add(route);
        }
      }
    }
    suggestions = [
      ...Array.from(stopSet.values()).map(obj => ({ type: 'Stop', value: obj.value, display: obj.display, displayKannada: obj.displayKannada })),
      ...Array.from(areaViaSet.values()),
      // ...Array.from(platformSet.values()),
      ...Array.from(routeSet.entries()).map(([r, obj]) => ({ type: 'Route', value: obj.value, display: obj.display })),
    ];
    setResults(Array.from(matched));
  } else {
    setResults(get(routes));
  }
</script>

<!-- Back button row (when search is active, sheet/sidebar is open, or showBackButton is true) -->
{#if showBackButton}
  <div class="cupertino-back-row">
    <button class="cupertino-back-text" on:click={handleBack} aria-label="Back">
      <span class="material-icons" aria-hidden="true">chevron_left</span>Back
    </button>
  </div>
{/if}

<!-- Flex row: search bar only -->
<div class="cupertino-bar-row">
  <div class="cupertino-bar-flex">
    <div class="cupertino-searchbar {searchFocused || voiceSearchActive ? 'cupertino-searchbar-focused' : ''}">
      <span class="material-icons cupertino-search-icon">search</span>
      <input
        bind:this={searchInput}
        class="cupertino-input"
        type="text"
        placeholder="Search by bus number or destination..."
        bind:value={$search}
        autofocus={searchFocused || voiceSearchActive}
        on:focus={() => searchFocused = true}
        autocomplete="off"
      />
      {#if $search}
        <button class="material-icons cupertino-clear" type="button" on:click={clearSearch} aria-label="Clear">close</button>
      {/if}
      {#if speechSupported}
        <button class="material-icons cupertino-mic" type="button" on:click={startVoiceSearch} aria-label="Voice Search">{recognizing ? 'mic' : 'mic_none'}</button>
      {/if}
    </div>
  </div>
</div>

{#if (searchFocused || voiceSearchActive) && $search && suggestions.length > 0}
  <Dropdown bind:this={dropdownRef} {suggestions} {$search} onSelect={handleSelectSuggestion} />
{/if}

<style>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');
.cupertino-back-row {
  width: 100%;
  display: flex;
  align-items: center;
  margin-bottom: 4px;
}
.cupertino-back-text {
  background: none;
  border: none;
  color: #007aff;
  font-size: 19px;
  font-weight: 500;
  font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;
  padding: 4px 12px 4px 0;
  cursor: pointer;
  border-radius: 8px;
  transition: background 0.15s;
  outline: none;
  text-align: left;
  display: flex;
  align-items: center;
}
.cupertino-back-text:active {
  background: #e5e5ea;
}
.cupertino-back-text .material-icons {
  font-size: 28px;
  margin-right: 2px;
  vertical-align: middle;
  line-height: 1;
}
.cupertino-bar-row {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
  position: relative;
  z-index: 100;
}
.cupertino-bar-flex {
  flex: 1 1 0%;
  display: flex;
}
.cupertino-searchbar {
  display: flex;
  align-items: center;
  background: #f1f1f3;
  border-radius: 14px;
  border: 1px solid #e0e0e5;
  box-shadow: 0 1px 6px 0 rgba(60,60,67,0.06);
  padding: 0 10px;
  height: 44px;
  width: 100%;
  font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;
  transition: box-shadow 0.2s, background 0.2s;
  position: relative;
  z-index: 100;
}

.cupertino-search-icon {
  color: #8e8e93;
  font-size: 22px;
  margin-right: 4px;
}
.cupertino-input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  font-size: 17px;
  color: #222;
  padding: 0 6px;
  font-family: inherit;
}
.cupertino-input::placeholder {
  color: #8e8e93;
  opacity: 1;
  font-weight: 400;
}
.cupertino-mic {
  background: none;
  border: none;
  color: #007aff;
  font-size: 22px;
  margin-left: 2px;
  cursor: pointer;
  padding: 4px;
}
.cupertino-clear {
  background: none;
  border: none;
  color: #8e8e93;
  font-size: 22px;
  margin-left: 2px;
  cursor: pointer;
  padding: 4px;
}
</style> 