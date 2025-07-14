<style>
  @import url('https://fonts.googleapis.com/icon?family=Material+Icons');
  @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600&display=swap');
  .routeview-sheet {
    background: #f5f5f7;
    border-radius: 10px 10px 0 0;
    padding: 0;
    font-family: 'Manrope', sans-serif;
    min-width: 0;
    max-width: 100%;
  }
  .routeview-header {
    display: flex;
    flex-direction: row;
    align-items: center;
    padding: 35px 30px 35px 30px;
    gap: 10px;
    flex: none;
    order: 1;
    flex-grow: 0;
  }
  .routeview-header-group {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    padding: 0;
    flex: none;
    order: 0;
    flex-grow: 0;
    min-width: 0;
    flex-shrink: 1;
  }
  .routeview-header-row {
    display: flex;
    flex-direction: row;
    align-items: center;
    padding-bottom: 15px;
    gap: 8px;
    flex: none;
    order: 0;
    flex-grow: 0;
    min-width: 0;
  }
  .platform-circle {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    padding: 2.01943px;
    gap: 2.02px;
    width: 29px;
    height: 29px;
    background: #F68511;
    border-radius: 20.1943px;
    color: #fff;
    font-family: 'Manrope', sans-serif;
    font-weight: 600;
    font-size: 14px;
    line-height: 19px;
    flex: none;
    order: 0;
    flex-grow: 0;
  }
  .routeview-destination {
    font-family: 'Manrope', sans-serif;
    font-style: normal;
    font-weight: 600;
    padding: 0;
    font-size: 20px;
    line-height: 27px;
    color: #1A1A1A;
    flex: none;
    order: 0;
    align-self: stretch;
    flex-grow: 0;
    flex-shrink: 1;
  }
  .routeview-via-row {
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    padding: 0;
    gap: 4px;
    flex: none;
    order: 1;
    align-self: stretch;
    flex-grow: 0;
  }
  .routeview-via-label {
    font-family: 'Manrope', sans-serif;
    font-style: normal;
    font-weight: 600;
    font-size: 16px;
    line-height: 22px;
    color: #585858;
    flex: none;
    order: 0;
    flex-grow: 0;
  }
  .stops-container {
    position: relative;
    margin-left: 33px;
    min-height: 0;
    margin-bottom: 24px;
  }
  /* .vertical-track {
    position: absolute;
    left: 0;
    top: 0;
    width: 22px;
    background: #E5E5E6;
    border-radius: 100px;
    z-index: 0;
    margin-top: -3px;
  } */
  .stops-list {
    display: flex;
    flex-direction: column;
    gap: 22px;
    align-items: flex-start;
    position: relative;
    z-index: 5;
  }
  .stop-row {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 16px;
    /*height: 19px;*/
  }
  .stop-circle {
    width: 7px;
    height: 7px;
    background: #CE242B;
    border-radius: 50%;
    /*box-shadow: 0 1px 4px rgba(0,0,0,0.04);*/
    flex-shrink: 0;
    /*margin-left: 2px;*/
  }
  .stop-icon {
    display: flex;
    align-items: center;
    width: 20px;
    height: 20px;
    margin-left: -6px;
    margin-right: -6px;
  }
  .stop-name {
    font-family: 'Manrope', sans-serif;
    font-size: 14px;
    /*line-height: 1px;*/
    color: #1A1A1A;
    font-weight: 400;
    word-break: break-word;
    /*max-width: 260px;*/
  }
  .previous-selected {
    font-family: 'Manrope', sans-serif;
    font-size: 14px;
    /*line-height: 19px;*/
    color: #1A1A1A;
    word-break: break-word;
    font-weight: 600;
  }
  .chevron-btn {
    background: none;
    border: none;
    padding: 0 8px 0 0;
    margin-right: -10px;
    margin-left: -28px;
    display: flex;
    align-items: center;
    height: 32px;
    width: 32px;
    cursor: pointer;
  }
  .material-icons {
    font-family: 'Material Icons';
    font-weight: 400;
    font-size: 32px;
    color: #3C3C434D;
    display: inline-block;
  }
  /*.chevron-btn svg {*/
  /*  display: block;*/
  /*}*/
</style>
<script lang="ts">
  import { platforms } from '$lib/stores/platforms';
  import {language} from "$lib/stores/language";
  import {messages} from "$lib/stores/messages";
  import { routes } from "$lib/stores/routes";
  import { selectedItem, previousSelectedItem } from '$lib/stores/selectedItem';
  import BusModal from './BusModal.svelte';
  import LocationStar from '../../assets/icons/location-star.svg';
  import {setResults} from "$lib/stores/results";
  import {tick} from "svelte";

  let findRoute = null;
  if ($selectedItem && $selectedItem.type === 'Route') {
    if ($selectedItem.value) {
      findRoute = $routes.find(r => r.number == $selectedItem.value);
      tick().then(() => setResults([findRoute]));
    } else {
      findRoute = $selectedItem;
    }
  }
  const pf = findRoute ? $platforms.find(p => p.platformNumber == findRoute.platformNumber) : null;
  const platformColor = pf ? pf.color : '#888';

  function isKempegowda(stop) {
    return stop.name === 'Kempegowda Bus Station';
  }
  function handleChevronClick() {
    if ($previousSelectedItem) {
      selectedItem.set($previousSelectedItem);
      previousSelectedItem.set(undefined);
    }
  }
  // const stopCount = findRoute?.stops?.length || 0;
  // const trackGap = 58.658;
  // const circleHeight = 19;
  // const trackHeight = stopCount > 1 ? (stopCount - 1) * trackGap + circleHeight : circleHeight;
  // console.log($previousSelectedItem);
</script>

{#if $selectedItem && $selectedItem.type === 'Route' && findRoute}
  <div class="routeview-sheet">
    <div class="routeview-header">
      <div class="routeview-header-group">
        <div class="routeview-header-row">
          {#if $previousSelectedItem}
            <button class="chevron-btn" on:click={handleChevronClick}>
              <span class="material-icons" aria-hidden="true">chevron_left</span>
            </button>
          {/if}
          <div class="platform-circle" style="background:{platformColor}">{findRoute.platformNumber}</div>
          <div class="routeview-header-busmodal">
            <BusModal number={findRoute.number} />
          </div>
        </div>
        <div class="routeview-destination">{$language === 'en' ? findRoute.destination : findRoute.kannadaDestination ?? findRoute.destination}</div>
        {#if findRoute.via?.name}
          <div class="routeview-via-row">
            <span class="routeview-via-label">{$messages.via().replace('%1', $language === 'en' ? findRoute.via?.name : findRoute.via?.nameKannada ?? findRoute.via?.name)}</span>
          </div>
        {/if}
      </div>
    </div>
    <div class="stops-container">
      <!-- <div class="vertical-track" style="height: {trackHeight}px;"></div> -->
      <div class="stops-list">
        {#each findRoute.stops as stop, i}
          <div class="stop-row">
            {#if isKempegowda(stop)}
              <span class="stop-icon">
                <LocationStar width="20" height="20" />
              </span>
            {:else}
              <div class="stop-circle"></div>
            {/if}
            <div class={$previousSelectedItem && $previousSelectedItem.type === 'Stop' && $previousSelectedItem.value.trim() === stop.name.trim() ? 'previous-selected' : 'stop-name'}>{$language === 'en' ? stop.name : stop.nameKannada}</div>
          </div>
        {/each}
      </div>
    </div>
  </div>
{:else}
  <div>Panic! Route not found or not selected.</div>
{/if}