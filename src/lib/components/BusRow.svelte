<script lang="ts">
  import BusModal from './BusModal.svelte';
  import {messages} from "$lib/stores/messages";
  import {language} from "$lib/stores/language";
  export let route;
  export let getPlatformColor;
  export let handleRouteClick;
</script>

<div class="busrow-card" on:click={() => handleRouteClick(route)} tabindex="0" role="button" aria-label={`View route ${route.number}`}>  
  <div class="busrow-top">
    <div class="platform-circle" style={`background:${getPlatformColor(route.platformNumber)}`}> 
      <span>{route.platformNumber}</span>
    </div>
    <BusModal number={route.number} />
    <span class="busrow-chevron">&#8250;</span>
  </div>
  <div class="busrow-body">
    <div class="busrow-dest">{$language === 'en' ? route.destination : route.kannadaDestination ?? route.destination}</div>
    <div class="busrow-via"><span class="via-label">{$messages.via().replace('%1', $language === 'en' ? route.via?.name : route.via?.nameKannada ?? route.via?.name)}</span> <span class="via-value"></span></div>
  </div>
</div>

<style>
.busrow-card {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 14px;
  gap: 8px;
  position: relative;
  min-width: 0;
  max-width: 100%;
  background: #EEEEEE;
  border-radius: 8px;
  cursor: pointer;
  transition: box-shadow 0.12s;
}
.busrow-top {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 8px;
  width: 100%;
  position: relative;
  margin-bottom: -2px;
}
.platform-circle {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  padding: 2px;
  gap: 2px;
  width: 29px;
  height: 29px;
  /*background: #DE3D82;*/
  border-radius: 20px;
  color: #fff;
  font-family: 'Manrope', sans-serif;
  font-weight: 600;
  font-size: 14px;
  /*line-height: 19px;*/
}
.busrow-chevron {
  margin-left: auto;
  width: 17px;
  height: 32px;
  display: flex;
  align-items: center;
  color: rgba(60, 60, 67, 0.3);
  font-size: 1.7rem;
}
.busrow-body {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
  /*width: 190px;*/
}
.busrow-dest {
  font-family: 'Manrope', sans-serif;
  font-size: 16px;
  font-weight: 400;
  color: #1A1A1A;
  padding-bottom: 1px;
}
.busrow-via {
  display: flex;
  flex-direction: row;
  gap: 4px;
  font-family: 'Manrope', sans-serif;
  font-size: 14px;
  color: #585858;
  line-height: 10px;
}
.via-label {
  font-weight: 400;
  color: #585858;
}
.via-value {
  font-weight: 400;
  color: #585858;
}
</style> 