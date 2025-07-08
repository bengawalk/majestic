<script lang="ts">
  export let number: string | number;
  import RouteIcon from '../../assets/icons/route.svg';
</script>

<div class="busmodal-outer">
  <div class="busmodal-inner">
    <span class="busmodal-icon">
      <RouteIcon width="14" height="16.8" />
    </span>
    <span class="busmodal-number">{number}</span>
  </div>
</div>

<style>
.busmodal-outer {
  /*display: flex;*/
  /*flex-direction: column;*/
  justify-content: center;
  align-items: center;
  padding: 4px;
  gap: 4.23px;
  height: 24.8px;
  background: rgba(118, 118, 128, 0.12);
  border-radius: 4px;
  flex: none;
  /*order: 1;*/
  flex-grow: 0;
}
.busmodal-inner {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 0px;
  gap: 4px;
  height: 16.8px;
  flex: none;
  /*order: 0;*/
  /* align-self: stretch; */
  flex-grow: 0;
}
.busmodal-icon {
  display: flex;
  height: 16.8px;
  flex: none;
  order: 0;
  flex-grow: 0;
}
.busmodal-number {
  display: flex;
  height: 12px;
  font-family: 'Manrope', sans-serif;
  font-style: normal;
  font-weight: 600;
  font-size: 16px;
  line-height: 22px;
  color: #000000;
  flex: none;
  order: 1;
  flex-grow: 0;
  align-items: center;
  justify-content: flex-start;
}
</style> 