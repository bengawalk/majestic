<script lang="ts">
  import { createEventDispatcher, onMount, tick } from 'svelte';
  import RouteView from './routeview.svelte';
  export let selectedItem: any = null;
  const dispatch = createEventDispatcher();
  let isWide = false;
  let paneInstance = null;
  let paneContentEl: HTMLDivElement | null = null;

  function checkWide() {
    isWide = window.innerWidth >= 500;
  }

  async function openPane() {
    if (!paneContentEl || isWide || !selectedItem) {
      console.log("CANCEL OPENING PANE");
      return;
    }
    const { CupertinoPane } = await import('cupertino-pane');
    if (paneInstance) {
      paneInstance.destroy();
      paneInstance = null;
    }
    // Calculate content height
    await tick();
    let contentHeight = paneContentEl.firstElementChild?.scrollHeight || 220;
    let maxHeight = window.innerHeight;
    paneInstance = new CupertinoPane(paneContentEl, {
      parentElement: 'body',
      breaks: {
        top: { enabled: true, height: Math.min(contentHeight + 40, maxHeight), bounce: true },
        middle: { enabled: false },
        bottom: { enabled: false }
      },
      initialBreak: 'top',
      backdrop: true, // No gray-out
      darkMode: false,
      buttonDestroy: false,
      onWillDismiss: () => { dispatch('close'); },
      onDidDismiss: () => { dispatch('close'); },
    });
    paneInstance.present();
  }

  function close() {
    if (isWide) {
      dispatch('close');
    } else if (paneInstance) {
      paneInstance.destroy();
      paneInstance = null;
    }
  }

  onMount(() => {
    checkWide();
    window.addEventListener('resize', checkWide);
    return () => {
      window.removeEventListener('resize', checkWide);
      if (paneInstance) paneInstance.destroy();
    };
  });

  $: if (!isWide && selectedItem) {
    console.log("Attempting to open pane");
    openPane();
  }
  $: if (!selectedItem && paneInstance) {
    console.log("Destroying pane");
    paneInstance.destroy();
    paneInstance = null;
  }
</script>

{#if selectedItem}
  {#if isWide}
    <div class="sheet-container is-wide sheet-open" role="dialog" aria-modal="true">
      <div class="sheet-content">
        <button class="sheet-close" aria-label="Close" on:click={close}>&times;</button>
        {#if selectedItem.type === 'Route'}
          <RouteView route={selectedItem} platformColor={selectedItem.platformColor || '#888'} />
        {:else}
          <h2>{selectedItem.display}</h2>
          {#if selectedItem.displayKannada}
            <div class="sheet-kannada">{selectedItem.displayKannada}</div>
          {/if}
          <div class="sheet-type">Type: {selectedItem.type}</div>
        {/if}
      </div>
    </div>
  {:else}
    <div bind:this={paneContentEl} style="display:none">
      <div class="sheet-content">
        <button class="sheet-close" aria-label="Close" on:click={close}>&times;</button>
        {#if selectedItem.type === 'Route'}
          <RouteView route={selectedItem} platformColor={selectedItem.platformColor || '#888'} />
        {:else}
          <h2>{selectedItem.display}</h2>
          {#if selectedItem.displayKannada}
            <div class="sheet-kannada">{selectedItem.displayKannada}</div>
          {/if}
          <div class="sheet-type">Type: {selectedItem.type}</div>
        {/if}
      </div>
    </div>
  {/if}
{/if}

<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600&display=swap');
.sheet-container {
  position: fixed;
  z-index: 1000;
  left: 0;
  right: 0;
  bottom: 0;
  top: auto;
  background: #f5f5f7;
  box-shadow: 0 -2px 24px rgba(0,0,0,0.08), 0px 0px 4px rgba(0,0,0,0.25);
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  transition: transform 0.2s cubic-bezier(.4,0,.2,1);
  max-height: 100vh;
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
  background: linear-gradient(0deg, rgba(61, 61, 61, 0.5), rgba(61, 61, 61, 0.5)), rgba(127, 127, 127, 0.2);
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
.sheet-kannada {
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
}
@media (min-width: 500px) {
  .sheet-container {
    left: 0;
    right: auto;
    top: 0;
    bottom: 0;
    width: 380px;
    max-width: 100vw;
    min-height: 100vh;
    border-radius: 0;
    box-shadow: 2px 0 24px rgba(0,0,0,0.08), 0px 0px 4px rgba(0,0,0,0.25);
    background: #f5f5f7;
    transition: transform 0.2s cubic-bezier(.4,0,.2,1);
  }
}
</style> 