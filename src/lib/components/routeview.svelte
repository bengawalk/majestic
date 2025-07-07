<style>
  @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600&display=swap');
  .routeview-sheet {
    background: #f5f5f7;
    border-radius: 10px 10px 0 0;
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
  .route-svg {
    display: flex;
    align-items: center;
    margin-right: 4px;
  }
  .route-destination-group {
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin-left: 12px;
  }
  .route-destination {
    font-size: 16px;
    font-weight: 400;
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
    min-height: 0;
    margin-bottom: 24px;
  }
  .vertical-track {
    position: absolute;
    left: 0;
    top: 0;
    width: 22px;
    background: #E5E5E6;
    border-radius: 100px;
    z-index: 0;
    margin-top: -3px;
  }
  .stops-list {
    display: flex;
    flex-direction: column;
    gap: 40px;
    align-items: flex-start;
    position: relative;
    z-index: 5;
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
  .stop-icon {
    display: flex;
    align-items: center;
    width: 20px;
    height: 20px;
    margin-left: 1px;
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
    margin-right: -20px;
    margin-left: -24px;
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

  let findRoute = null;
  if ($selectedItem && $selectedItem.type === 'Route') {
    if ($selectedItem.value) {
      findRoute = $routes.find(r => r.number == $selectedItem.value);
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
  const stopCount = findRoute?.stops?.length || 0;
  const trackGap = 58.658;
  const circleHeight = 19;
  const trackHeight = stopCount > 1 ? (stopCount - 1) * trackGap + circleHeight : circleHeight;
</script>

{#if $selectedItem && $selectedItem.type === 'Route' && findRoute}
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
        <span class="route-svg" aria-label="Route icon">
          <svg width="16" height="21" viewBox="0 0 16 21" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M0 3.85373C0 2.22976 1.30971 0.899902 2.90908 0.899902H13.0909C14.6903 0.899902 16 2.22976 16 3.85373V15.6691C16 17.1461 14.5455 17.146 14.5455 17.146V18.623C14.5455 19.436 13.8917 20.0999 13.0909 20.0999C12.2902 20.0999 11.6364 19.436 11.6364 18.623V17.146H4.36364V18.623C4.36364 19.436 3.70982 20.0999 2.90908 20.0999C2.10833 20.0999 1.45456 19.436 1.45456 18.623V17.146C1.64986e-05 17.146 0 15.6691 0 15.6691V3.85373ZM2.18289 5.33067C1.77612 5.33067 1.45456 5.65501 1.45456 6.07019V10.501C1.45456 10.914 1.77399 11.2405 2.18289 11.2405H13.8192C14.226 11.2405 14.5476 10.9161 14.5476 10.501V6.07019C14.5476 5.65717 14.2281 5.33067 13.8192 5.33067H2.18289ZM2.90908 12.7153C2.10833 12.7153 1.45456 13.3791 1.45456 14.1922C1.45456 15.0053 2.10833 15.6691 2.90908 15.6691C3.70982 15.6691 4.36364 15.0053 4.36364 14.1922C4.36364 13.3791 3.70982 12.7153 2.90908 12.7153ZM13.0909 12.7153C12.2902 12.7153 11.6364 13.3791 11.6364 14.1922C11.6364 15.0053 12.2902 15.6691 13.0909 15.6691C13.8917 15.6691 14.5455 15.0053 14.5455 14.1922C14.5455 13.3791 13.8917 12.7153 13.0909 12.7153ZM2.90908 3.1142C2.90908 3.52722 3.22856 3.85373 3.63532 3.85373H12.3626C12.7694 3.85373 13.0909 3.52938 13.0909 3.1142C13.0909 2.69902 12.7715 2.37679 12.3626 2.37679H3.63532C3.23069 2.37679 2.90908 2.70118 2.90908 3.1142Z" fill="black"/>
          </svg>
        </span>
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
      <div class="vertical-track" style="height: {trackHeight}px;"></div>
      <div class="stops-list">
        {#each findRoute.stops as stop, i}
          <div class="stop-row">
            {#if isKempegowda(stop)}
              <span class="stop-icon">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <rect x="1" y="1" width="18" height="18" rx="9" fill="#FAFAFA"/>
                  <rect x="1" y="1" width="18" height="18" rx="9" stroke="#CE242B" stroke-width="1.22705" stroke-miterlimit="10"/>
                  <path d="M9.90879 4.17643C9.96126 4.17643 10.0154 4.17643 10.0678 4.17643C10.24 4.23052 10.3236 4.36167 10.3974 4.5174C10.891 5.57965 11.3928 6.64026 11.888 7.70087C11.9175 7.7648 11.9535 7.80251 12.0273 7.81234C12.1962 7.83201 12.3651 7.85988 12.5324 7.88611C13.4933 8.03201 14.4541 8.18282 15.415 8.3238C15.6085 8.35167 15.7479 8.43035 15.8233 8.61395C15.8233 8.6828 15.8233 8.75001 15.8233 8.81886C15.7676 8.88771 15.7167 8.96312 15.6544 9.02705C14.8329 9.86636 14.0131 10.7073 13.1932 11.5483C13.1555 11.5876 13.1161 11.6187 13.1292 11.6909C13.2785 12.5761 13.4211 13.4613 13.5654 14.3465C13.6195 14.6793 13.6753 15.012 13.7277 15.3448C13.7589 15.5415 13.6982 15.6841 13.5539 15.7645C13.5162 15.7858 13.4752 15.8038 13.4359 15.8218C13.39 15.8218 13.344 15.8218 13.2998 15.8218C13.2342 15.7858 13.1686 15.7497 13.1046 15.7137C12.0995 15.1612 11.096 14.6071 10.0941 14.0498C10.0269 14.0121 9.97766 14.0121 9.90879 14.0498C9.48738 14.2875 9.06269 14.5219 8.638 14.7547C7.98538 15.1104 7.3426 15.4874 6.67851 15.8235C6.6326 15.8235 6.58668 15.8235 6.54241 15.8235C6.31449 15.7153 6.23742 15.5481 6.28005 15.2907C6.48174 14.1072 6.66703 12.922 6.86544 11.7384C6.8802 11.645 6.85396 11.5925 6.79493 11.5319C6.1292 10.8516 5.46346 10.1729 4.80101 9.48932C4.58784 9.26966 4.35664 9.06803 4.17627 8.81886C4.17627 8.74345 4.17627 8.66641 4.17627 8.591C4.25334 8.47297 4.33532 8.36478 4.4911 8.34183C5.64056 8.16807 6.78837 7.99102 7.93783 7.8189C8.02965 7.80579 8.08049 7.77136 8.12148 7.68448C8.60684 6.6419 9.09876 5.6026 9.58413 4.56002C9.65955 4.39773 9.73498 4.24692 9.90879 4.17643Z" fill="#CE242B"/>
                </svg>
              </span>
            {:else}
              <div class="stop-circle"></div>
            {/if}
            <div class="stop-name {isKempegowda(stop) ? 'kempegowda-label' : ''}">{stop.name}</div>
          </div>
        {/each}
      </div>
    </div>
  </div>
{:else}
  <div>Route not found or not selected.</div>
{/if}