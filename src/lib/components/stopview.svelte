<script lang="ts">
  import { get } from 'svelte/store';
  import { platforms } from '$lib/stores/platforms';
  import { routes as allRoutes } from '$lib/stores/routes';
  import { selectedItem, previousSelectedItem } from '$lib/stores/selectedItem';

  // Helper to get platform color
  function getPlatformColor(platformNumber) {
    const pf = get(platforms).find(p => p.platformNumber == platformNumber);
    return pf ? pf.color : '#F68511';
  }
  // Filtering logic
  const all = get(allRoutes);
  let mainRoutes = [];
  let areaRoutes = [];

  if ($selectedItem) {
    if($selectedItem.type === 'Platform') {
      console.log($selectedItem);
      mainRoutes = all.filter(r => r.platformNumber.trim() === $selectedItem.display.trim());
    }
    if ($selectedItem.type === 'Stop') {
      mainRoutes = all.filter(r => r.stops && r.stops.some(s => s.name === $selectedItem.display));
      areaRoutes = all.filter(r => ((r.area && r.area.name.trim() === $selectedItem.display.trim()) || (r.via && r.via.name.trim() === $selectedItem.display.trim())) && !mainRoutes.includes(r));
      // console.log("ROUTES", mainRoutes, areaRoutes);
    } else if ($selectedItem.type === 'Area') {
      mainRoutes = all.filter(r => ((r.area && r.area.name === $selectedItem.display) || (r.via && r.via.name === $selectedItem.display)));
    }
  }

  function handleRouteClick(route) {
    previousSelectedItem.set($selectedItem);
    selectedItem.set({ value: route.number, type: 'Route' });
  }
</script>

{#if $selectedItem && ($selectedItem.type === 'Stop' || $selectedItem.type === 'Platform' || $selectedItem.type === 'Area')}
  <div class="stopview-content">
    <div class="stopview-header">{$selectedItem.type === 'Platform' ? 'Platform' : 'To'} {$selectedItem?.display}</div>
    <div class="stopview-list">
      {#each mainRoutes as route}
        <div class="route-row" on:click={() => handleRouteClick(route)} tabindex="0" role="button" aria-label="View route {route.number}">
          <div class="platform-circle" style="background:{getPlatformColor(route.platformNumber)}">
            <span>{route.platformNumber}</span>
          </div>
          <div class="bus-modal">
            <span class="bus-icon">
                        <svg width="16" height="21" viewBox="0 0 16 21" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M0 3.85373C0 2.22976 1.30971 0.899902 2.90908 0.899902H13.0909C14.6903 0.899902 16 2.22976 16 3.85373V15.6691C16 17.1461 14.5455 17.146 14.5455 17.146V18.623C14.5455 19.436 13.8917 20.0999 13.0909 20.0999C12.2902 20.0999 11.6364 19.436 11.6364 18.623V17.146H4.36364V18.623C4.36364 19.436 3.70982 20.0999 2.90908 20.0999C2.10833 20.0999 1.45456 19.436 1.45456 18.623V17.146C1.64986e-05 17.146 0 15.6691 0 15.6691V3.85373ZM2.18289 5.33067C1.77612 5.33067 1.45456 5.65501 1.45456 6.07019V10.501C1.45456 10.914 1.77399 11.2405 2.18289 11.2405H13.8192C14.226 11.2405 14.5476 10.9161 14.5476 10.501V6.07019C14.5476 5.65717 14.2281 5.33067 13.8192 5.33067H2.18289ZM2.90908 12.7153C2.10833 12.7153 1.45456 13.3791 1.45456 14.1922C1.45456 15.0053 2.10833 15.6691 2.90908 15.6691C3.70982 15.6691 4.36364 15.0053 4.36364 14.1922C4.36364 13.3791 3.70982 12.7153 2.90908 12.7153ZM13.0909 12.7153C12.2902 12.7153 11.6364 13.3791 11.6364 14.1922C11.6364 15.0053 12.2902 15.6691 13.0909 15.6691C13.8917 15.6691 14.5455 15.0053 14.5455 14.1922C14.5455 13.3791 13.8917 12.7153 13.0909 12.7153ZM2.90908 3.1142C2.90908 3.52722 3.22856 3.85373 3.63532 3.85373H12.3626C12.7694 3.85373 13.0909 3.52938 13.0909 3.1142C13.0909 2.69902 12.7715 2.37679 12.3626 2.37679H3.63532C3.23069 2.37679 2.90908 2.70118 2.90908 3.1142Z" fill="black"/>
          </svg>
            </span>
            <span class="route-number">{route.number}</span>
          </div>
          <div class="route-body">
            <div class="route-dest">{route.destination}</div>
            <div class="route-via">
              <span class="via-label">Via</span>
              <span class="via-value">{route.via?.name}</span>
            </div>
          </div>
          <span class="chevron">&#8250;</span>
        </div>
      {/each}
    </div>
    {#if $selectedItem?.type === 'Stop' && areaRoutes.length}
      <div class="section-header">Other buses going to {$selectedItem?.display} Area</div>
      <div class="stopview-list">
        {#each areaRoutes as route}
          <div class="route-row" on:click={() => handleRouteClick(route)} tabindex="0" role="button" aria-label="View route {route.number}">
            <div class="platform-circle" style="background:{getPlatformColor(route.platformNumber)}">
              <span>{route.platformNumber}</span>
            </div>
            <div class="bus-modal">
              <span class="bus-icon">
                        <svg width="16" height="21" viewBox="0 0 16 21" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M0 3.85373C0 2.22976 1.30971 0.899902 2.90908 0.899902H13.0909C14.6903 0.899902 16 2.22976 16 3.85373V15.6691C16 17.1461 14.5455 17.146 14.5455 17.146V18.623C14.5455 19.436 13.8917 20.0999 13.0909 20.0999C12.2902 20.0999 11.6364 19.436 11.6364 18.623V17.146H4.36364V18.623C4.36364 19.436 3.70982 20.0999 2.90908 20.0999C2.10833 20.0999 1.45456 19.436 1.45456 18.623V17.146C1.64986e-05 17.146 0 15.6691 0 15.6691V3.85373ZM2.18289 5.33067C1.77612 5.33067 1.45456 5.65501 1.45456 6.07019V10.501C1.45456 10.914 1.77399 11.2405 2.18289 11.2405H13.8192C14.226 11.2405 14.5476 10.9161 14.5476 10.501V6.07019C14.5476 5.65717 14.2281 5.33067 13.8192 5.33067H2.18289ZM2.90908 12.7153C2.10833 12.7153 1.45456 13.3791 1.45456 14.1922C1.45456 15.0053 2.10833 15.6691 2.90908 15.6691C3.70982 15.6691 4.36364 15.0053 4.36364 14.1922C4.36364 13.3791 3.70982 12.7153 2.90908 12.7153ZM13.0909 12.7153C12.2902 12.7153 11.6364 13.3791 11.6364 14.1922C11.6364 15.0053 12.2902 15.6691 13.0909 15.6691C13.8917 15.6691 14.5455 15.0053 14.5455 14.1922C14.5455 13.3791 13.8917 12.7153 13.0909 12.7153ZM2.90908 3.1142C2.90908 3.52722 3.22856 3.85373 3.63532 3.85373H12.3626C12.7694 3.85373 13.0909 3.52938 13.0909 3.1142C13.0909 2.69902 12.7715 2.37679 12.3626 2.37679H3.63532C3.23069 2.37679 2.90908 2.70118 2.90908 3.1142Z" fill="black"/>
          </svg>
              </span>
              <span class="route-number">{route.number}</span>
            </div>
            <div class="route-body">
              <div class="route-dest">{route.destination}</div>
              <div class="route-via">
                <span class="via-label">Via</span>
                <span class="via-value">{route.via?.name}</span>
              </div>
            </div>
            <span class="chevron">&#8250;</span>
          </div>
        {/each}
      </div>
    {/if}
  </div>
{:else}
  <div>selectedItem is undefined or not a stop/area/via/destination</div>
{/if}

<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600&display=swap');
.stopview-content {
  padding: 32px 20px 20px 20px;
}
.stopview-header {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 24px;
}
.section-header {
  font-size: 16px;
  font-weight: 500;
  margin: 32px 0 12px 0;
  color: #222;
}
.stopview-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.route-row {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding: 10px 0;
  gap: 15px;
  width: 100%;
}
.platform-circle {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  font-size: 1rem;
  font-weight: 600;
  color: #fff;
}
.bus-modal {
  display: flex;
  flex-direction: row;
  align-items: center;
  background: rgba(118, 118, 128, 0.12);
  border-radius: 4px;
  padding: 4px 12px 4px 8px;
  gap: 8px;
  min-width: 60px;
  height: 27.2px;
}
.bus-icon {
  display: flex;
  align-items: center;
  margin-right: 4px;
}
.route-number {
  font-size: 1.1rem;
  font-weight: 600;
  color: #000;
}
.route-body {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  min-width: 120px;
  max-width: 190px;
  flex: 1 1 0;
}
.route-dest {
  font-size: 16px;
  font-weight: 400;
  color: #1A1A1A;
  margin-bottom: 2px;
}
.route-via {
  display: flex;
  flex-direction: row;
  gap: 4px;
  font-size: 14px;
  color: #585858;
}
.via-label {
  font-weight: 400;
  color: #585858;
}
.via-value {
  font-weight: 400;
  color: #585858;
}
.chevron {
  font-size: 1.7rem;
  color: rgba(60,60,67,0.3);
  margin-left: 8px;
  user-select: none;
}
</style> 