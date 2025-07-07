<script lang="ts">
import Map from '$lib/components/map.svelte';
import Header from '$lib/components/header.svelte';
import SearchBar from '$lib/components/searchbar.svelte';
import { onMount, tick } from 'svelte';
import SidebarSheet from '$lib/components/sidebar.svelte';
import {previousSelectedItem, selectedItem} from "$lib/stores/selectedItem";

let search = '';
let searchFocused = false;
let searchInput: HTMLInputElement | null = null;
let recognizing = false;
let recognition: SpeechRecognition | null = null;
let speechSupported = false;
let voiceSearchActive = false;

let overlayRef: HTMLDivElement | null = null;
// let blurHeight = 110;
let overlayTop = 16; // px

// Compute overlay left margin for desktop reactivity
$: overlayLeft = (typeof window !== 'undefined' && window.innerWidth >= 600 && $selectedItem) ? '180px' : '0';

// async function updateBlur() {
//     await tick();
//     if (overlayRef) {
//         blurHeight = overlayRef.offsetHeight + 16;
//     }
// }

onMount(() => {
    // updateBlur();
    // window.addEventListener('resize', updateBlur);
    // return () => window.removeEventListener('resize', updateBlur);
});

$: overlayTop = (searchFocused || voiceSearchActive) ? 24 : 16;
// $:  updateBlur(); // re-measure on every state change

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

function openSheet(item) {
    selectedItem.set(undefined);
    selectedItem.set(item);
}

function closeSheet() {
  selectedItem.set(undefined);
  previousSelectedItem.set(undefined);
}
</script>

<!-- Centered floating header and search overlay, always visible at the top -->
<div class="absolute left-0 w-full z-100 flex flex-col items-center pointer-events-none" style="top: {overlayTop}px; margin-left: {overlayLeft}; transition: margin-left 0.2s cubic-bezier(.4,0,.2,1);">
    <div bind:this={overlayRef} class="w-full max-w-2xl mx-auto flex flex-col items-stretch pointer-events-auto relative" style="z-index:100;">
        {#if !(searchFocused || voiceSearchActive || $selectedItem || search)}
            <Header title="Majestic Bus Station" />
        {/if}
        <SearchBar
            bind:search
            bind:searchFocused
            {speechSupported}
            {recognizing}
            bind:searchInput
            {voiceSearchActive}
            {selectedItem}
            sidebarOpen={!!$selectedItem}
            showBackButton={!!search || searchFocused || voiceSearchActive || $selectedItem}
            on:select={e => openSheet(e.detail)}
            on:closeSheet={closeSheet}
        />
    </div>
</div>

<SidebarSheet />
<Map />

<style>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');
/*.cupertino-bar-row {*/
/*  display: flex;*/
/*  flex-direction: row;*/
/*  align-items: center;*/
/*  gap: 0.5rem;*/
/*  width: 100%;*/
/*  position: relative;*/
/*}*/
/*.cupertino-bar-flex {*/
/*  flex: 1 1 0%;*/
/*  display: flex;*/
/*}*/
.app-grid {
    display: block;
    width: 100vw;
    height: 100vh;
    z-index: 1;
}
.searchbar-sidebar-row {
    width: 100vw;
    left: 0;
    right: 0;
    pointer-events: auto;
    position: static;
    z-index: auto;
}
.sidebar-container {
    display: none;
}
@media (min-width: 600px) {
    .sidebar-container {
        display: block;
        min-width: 380px;
        max-width: 380px;
        height: 100vh;
    }
    .searchbar-overlay {
        width: auto;
        flex: 1;
        pointer-events: auto;
    }
    .searchbar-inner {
        max-width: 672px;
        width: 100%;
    }
}
.searchbar-overlay {
    width: 100vw;
    pointer-events: auto;
}
.searchbar-inner {
    width: 100vw;
    max-width: 100vw;
    pointer-events: auto;
    display: flex;
    flex-direction: column;
    align-items: stretch;
    overflow: visible;
}
</style>
