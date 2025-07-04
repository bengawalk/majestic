<style>
  @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600&display=swap');
  .routeview-sheet {
    background: #f5f5f7;
    border-radius: 10px 10px 0 0;
    filter: drop-shadow(0px 0px 4px rgba(0,0,0,0.25));
    padding: 0;
    font-family: 'Manrope', sans-serif;
  }
  .routeview-header {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 12px;
    padding: 35px 0 0 0;
    margin-left: 33px;
    margin-bottom: 18px;
  }
  .platform-circle {
    width: 29px;
    height: 29px;
    background: #F68511;
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-family: 'Manrope', sans-serif;
    font-weight: 600;
    font-size: 14px;
    line-height: 19px;
    flex-shrink: 0;
  }
  .route-badge {
    display: flex;
    flex-direction: row;
    align-items: center;
    background: rgba(118, 118, 128, 0.12);
    border-radius: 4px;
    padding: 4px 8px;
    gap: 4px;
    height: 27.2px;
    font-weight: 600;
    font-size: 16px;
    color: #000;
  }
  .bus-icon {
    font-size: 16px;
    margin-right: 4px;
  }
  .route-destination-group {
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin-left: 12px;
  }
  .route-destination {
    font-size: 20px;
    font-weight: 600;
    color: #1A1A1A;
    line-height: 25px;
  }
  .route-via {
    font-size: 14px;
    color: #585858;
    font-weight: 400;
    line-height: 19px;
  }
  .stops-container {
    position: relative;
    margin-left: 33px;
    min-height: 465px;
    margin-bottom: 24px;
  }
  .vertical-track {
    position: absolute;
    left: 0;
    top: 0;
    width: 22px;
    height: 100%;
    background: #E5E5E6;
    border-radius: 100px;
    z-index: 0;
    margin-top: -2px;
  }
  .stops-list {
    display: flex;
    flex-direction: column;
    gap: 22px;
    align-items: flex-start;
    position: relative;
    z-index: 1;
  }
  .stop-row {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 17px;
    height: 18px;
  }
  .stop-circle {
    width: 18px;
    height: 18px;
    background: #fff;
    border-radius: 50%;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    flex-shrink: 0;
    margin-left: 2px;
  }
  .stop-circle.kempegowda {
    background: #1976d2;
  }
  .stop-name {
    font-family: 'Manrope', sans-serif;
    font-size: 14px;
    line-height: 19px;
    color: #1A1A1A;
    font-weight: 400;
    word-break: break-word;
    max-width: 260px;
  }
  .chevron-btn {
    background: none;
    border: none;
    padding: 0 8px 0 0;
    margin-right: 0;
    margin-left: -8px;
    display: flex;
    align-items: center;
    height: 32px;
    width: 32px;
    cursor: pointer;
  }
  .chevron-btn svg {
    display: block;
  }
</style>
<script lang="ts">

  import { platforms } from '$lib/stores/platforms';
  import { get } from 'svelte/store';
  import { routes } from "$lib/stores/routes";
  import { selectedItem, previousSelectedItem } from '$lib/stores/selectedItem';
  export let route: any = null;

  // Find the route details
  const findRoute = route && route.value
    ? get(routes).find(r => r.number == route.value)
    : route;
  const pf = $platforms.find(p => p.platformNumber == findRoute.platformNumber);
  const platformColor = pf ? pf.platformColor : '#888';

  // Helper to check if a stop is the special one
  function isKempegowda(stop) {
    return stop.name === 'Kempegowda Bus Station';
  }

  // Chevron click handler
  function handleChevronClick() {
    if ($previousSelectedItem) {
      selectedItem.set($previousSelectedItem);
      previousSelectedItem.set(undefined);
    }
  }
</script>

{#if findRoute}
  <div class="routeview-sheet">
    <div class="routeview-header">
      {#if $previousSelectedItem}
        <button class="chevron-btn" aria-label="Back" on:click={handleChevronClick}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M15 19L8 12L15 5" stroke="#3C3C43" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      {/if}
      <div class="platform-circle" style="background:{platformColor}">{findRoute.platformNumber}</div>
      <div class="route-badge">
        <span class="bus-icon">b</span>
        <span class="route-number">{findRoute.number}</span>
      </div>
      <div class="route-destination-group">
        <div class="route-destination">{findRoute.destination}</div>
        {#if findRoute.via?.name}
          <div class="route-via">Via {findRoute.via.name}</div>
        {/if}
      </div>
    </div>
    <div class="stops-container">
      <div class="vertical-track"></div>
      <div class="stops-list">
        {#each findRoute.stops as stop}
          <div class="stop-row">
            <div class="stop-circle {isKempegowda(stop) ? 'kempegowda' : ''}"></div>
            <div class="stop-name {isKempegowda(stop) ? 'kempegowda-label' : ''}">{stop.name}</div>
          </div>
        {/each}
      </div>
    </div>
  </div>
{/if}