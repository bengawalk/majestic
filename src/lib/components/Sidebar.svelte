<script lang="ts">
  import { createEventDispatcher, onMount, tick } from 'svelte';
  import RouteView from './RouteView.svelte';
  import StopView from './StopView.svelte';
  import { search } from '$lib/stores/search'; // adjust path if needed
  import { selectedItem } from '$lib/stores/selectedItem';
  import {setResults} from "$lib/stores/results";
  import {routes} from "$lib/stores/routes";
  const dispatch = createEventDispatcher();
  let isWide = false;
  let paneInstance = null;
  let paneContentEl: HTMLDivElement | null = null;

  function checkWide() {
    isWide = window.innerWidth >= 1088;
  }

  async function openPane() {
    await tick();
    if (!paneContentEl || isWide || !$selectedItem) {
      return;
    }
    const { CupertinoPane } = await import('cupertino-pane');
    if (paneInstance) {
      paneInstance.destroy();
      paneInstance = null;
    }
    paneInstance = new CupertinoPane(paneContentEl, {
      parentElement: 'body',
      breaks: {
        top: { enabled: true, height:  Math.floor(window.innerHeight * 0.95), bounce: true },
        middle: { enabled: true, height: Math.floor(window.innerHeight * 0.5), bounce: true },
        bottom: { enabled: false, height: Math.floor(window.innerHeight * 0.2), bounce: true }
      },
      initialBreak: 'middle',
      backdrop: false,
      buttonDestroy: false,
      bottomClose: false,
    });
    paneInstance.present();
    paneInstance.paneEl.style.maxWidth = '100%';
    paneInstance.paneEl.style.zIndex = '1000'
  }

  function close() {
    if (isWide) {
      dispatch('close');
    } else if (paneInstance) {
      paneInstance.destroy();
      paneInstance = null;
    }
    search.set('');
    selectedItem.set(undefined);
    tick().then(() => setResults($routes))
  }

  onMount(() => {
    checkWide();
    window.addEventListener('resize', checkWide);
    return () => {
      window.removeEventListener('resize', checkWide);
      if (paneInstance) paneInstance.destroy();
    };
  });

  $: if (isWide && paneInstance || paneInstance && !$selectedItem) {
    paneInstance.destroy();

    paneInstance = null;
  }

  $: if (!isWide && selectedItem) {
    tick().then(() => {
      if (paneContentEl) {
        // if (paneInstance) {
        //   paneInstance.destroy();
        //   paneInstance = null;
        // }
        openPane();
      }
    });
  }
</script>

{#if $selectedItem}
  {#if isWide}
    <div class="sheet-container is-wide sheet-open" role="dialog" aria-modal="true">
      <div class="sheet-content">
        <button class="sheet-close" aria-label="Close" on:click={close}>&times;</button>
        {#if $selectedItem.type === 'Route'}
          <RouteView route={$selectedItem} />
        {:else if $selectedItem.type === 'Stop' || $selectedItem.type === 'Area' || $selectedItem.type === 'Platform'}
          <StopView selectedItem={$selectedItem} />
        {:else}
          <h2>{$selectedItem.display}</h2>
          {#if $selectedItem.displayKannada}
            <div class="sheet-secondary">{$selectedItem.displayKannada}</div>
          {/if}
        {/if}
      </div>
    </div>
  {:else}
    <div class="sheet-container sheet-open" bind:this={paneContentEl}>
      <div class="grabber"></div>
      <div class="sheet-content">
        <button class="sheet-close" aria-label="Close" on:click={close}>&times;</button>
        {#if $selectedItem.type === 'Route'}
          <RouteView route={$selectedItem} />
        {:else if $selectedItem.type === 'Stop' || $selectedItem.type === 'Area' || $selectedItem.type === 'Platform'}
          <StopView selectedItem={$selectedItem} />
        {:else}
          <h2>{$selectedItem.display}</h2>
          {#if $selectedItem.displayKannada}
            <div class="sheet-secondary">{$selectedItem.displayKannada}</div>
          {/if}
        {/if}
      </div>
    </div>
  {/if}
{/if}

<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600&display=swap');
.sheet-container {
  position: fixed;
  z-index: 100;
  left: 0;
  right: 0;
  bottom: 0;
  top: auto;
  background: #f5f5f7;
  box-shadow: 0 -2px 24px rgba(0,0,0,0.08), 0px 0px 4px rgba(0,0,0,0.25);
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  transition: transform 0.2s cubic-bezier(.4,0,.2,1);
  max-height: var(--app-height); /* --app-height is set by JS to match the visible viewport height, avoiding browser chrome issues on mobile. */
  min-height: 220px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  pointer-events: auto;
  font-family: 'Manrope', sans-serif;
}
.sheet-content {
  padding: 0;
  flex: 1;
  overflow-y: auto;
  position: relative;
}
.sheet-close {
  position: absolute;
  right: 18px;
  top: 18px;
  font-size: 28px;
  /*background: linear-gradient(0deg, rgba(61, 61, 61, 0.5), rgba(61, 61, 61, 0.5)), rgba(127, 127, 127, 0.2);*/
  background-blend-mode: overlay, luminosity;
  border-radius: 1000px;
  border: none;
  color: #888;
  cursor: pointer;
  z-index: 2;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.sheet-secondary {
  font-size: 18px;
  color: #888;
  margin-bottom: 12px;
}
.sheet-type {
  font-size: 15px;
  color: #444;
}
.sheet-open {
  transform: translateY(0);
  z-index: 100;
}
@media (min-width: 1088px) {
  .sheet-container {
    left: 0;
    right: auto;
    top: 0;
    bottom: 0;
    width: 380px;
    max-width: 100vw;
    min-height: var(--app-height);
    border-radius: 0;
    box-shadow: 2px 0 24px rgba(0,0,0,0.08), 0px 0px 4px rgba(0,0,0,0.25);
    background: #f5f5f7;
    transition: transform 0.2s cubic-bezier(.4,0,.2,1);
  }
}
</style> 