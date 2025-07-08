<script lang="ts">
  import { get } from 'svelte/store';
  import { platforms } from '$lib/stores/platforms';
  import { routes as allRoutes } from '$lib/stores/routes';
  import { selectedItem, previousSelectedItem } from '$lib/stores/selectedItem';
  import {language} from "$lib/stores/language";
  import {messages} from "$lib/stores/messages";
  import BusRow from './BusRow.svelte';

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
      // console.log($selectedItem);
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
    <div class="stopview-header">{$selectedItem.type === 'Platform' ? $messages.platform().replace('%1', $language === 'en' ? $selectedItem?.display : $selectedItem?.displayKannada ?? $selectedItem?.display) : $messages.buses_to().replace('%1', $language === 'en' ? $selectedItem?.display : $selectedItem?.displayKannada ?? $selectedItem?.display)}</div>
    <div class="stopview-list">
      {#each mainRoutes as route}
        <BusRow {route} {getPlatformColor} {handleRouteClick} />
      {/each}
    </div>
    {#if $selectedItem?.type === 'Stop' && areaRoutes.length}
      <div class="section-header">{$messages.other_buses_to().replace('%1', $language === 'en' ? $selectedItem?.display : $selectedItem?.displayKannada ?? $selectedItem?.display)}</div>
      <div class="stopview-list">
        {#each areaRoutes as route}
          <BusRow {route} {getPlatformColor} {handleRouteClick} />
        {/each}
      </div>
    {/if}
  </div>
{:else}
  <div>Panic: selectedItem is undefined or not a stop/area/platform</div>
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
</style> 