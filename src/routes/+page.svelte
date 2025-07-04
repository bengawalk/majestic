<script lang="ts">
import Map from '$lib/components/map.svelte';
import Header from '$lib/components/header.svelte';
import SearchBar from '$lib/components/searchbar.svelte';
import { onMount, tick } from 'svelte';

let search = '';
let searchFocused = false;
let searchInput: HTMLInputElement | null = null;
let recognizing = false;
let recognition: SpeechRecognition | null = null;
let speechSupported = false;
let voiceSearchActive = false;

let overlayRef: HTMLDivElement | null = null;
let blurHeight = 110;
let overlayTop = 16; // px

async function updateBlur() {
    await tick();
    if (overlayRef) {
        blurHeight = overlayRef.offsetHeight + 16;
    }
}

onMount(() => {
    updateBlur();
    window.addEventListener('resize', updateBlur);
    return () => window.removeEventListener('resize', updateBlur);
});

$: overlayTop = (searchFocused || voiceSearchActive) ? 24 : 16;
$: updateBlur(); // re-measure on every state change

if (typeof window !== 'undefined') {
    speechSupported = 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window;
    if (speechSupported && !recognition) {
        const SpeechRecognitionClass = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition;
        recognition = new SpeechRecognitionClass();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-IN';
        recognition.onstart = () => voiceSearchActive = true;
        recognition.onresult = (event: any) => {
            if (event.results && event.results[0] && event.results[0][0]) {
                search = event.results[0][0].transcript;
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
}
</script>

<!-- Full-width blur gradient behind header and search bar, always starts at top:0, height matches overlay -->
<div class="cupertino-blur-gradient" style="height: {blurHeight}px; top: 0;"></div>

<!-- Centered floating header and search overlay, top moves with overlay -->
<div class="absolute left-0 w-full z-30 flex flex-col items-center pointer-events-none" style="top: {overlayTop}px;">
    <div bind:this={overlayRef} class="w-full max-w-2xl mx-auto flex flex-col items-stretch pointer-events-auto relative" style="z-index:11;">
        {#if !(searchFocused || voiceSearchActive)}
            <Header title="Majestic Bus Station" />
        {/if}
        <SearchBar
            bind:search
            bind:searchFocused
            {speechSupported}
            {recognizing}
            bind:searchInput
            {voiceSearchActive}
        />
    </div>
</div>

<Map />

<style>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');
.cupertino-blur-gradient {
  position: fixed;
  left: 0;
  top: 0;
  width: 100vw;
  z-index: 2;
  pointer-events: none;
  background: linear-gradient(to bottom, rgba(250,250,252,0.95) 0%, rgba(250,250,252,0.7) 60%, rgba(250,250,252,0.0) 100%);
  backdrop-filter: blur(16px);
  transition: height 0.2s;
}
.cupertino-bar-row {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
  position: relative;
}
.cupertino-bar-flex {
  flex: 1 1 0%;
  display: flex;
}
</style>
