<script lang="ts">
  export let title: string = 'Majestic Bus Station';
</script>

<header class="cupertino-header">
  <h1>{title}</h1>
</header>

<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400&display=swap');
.cupertino-header {
  margin-top: 24px;
  margin-bottom: 18px;
  width: 100%;
  display: flex;
  align-items: center;
  z-index: 10;
  position: relative;
  padding-left: 24px;
  padding-right: 24px;
}
.cupertino-header h1 {
  font-size: 32px;
  font-weight: 400;
  color: #222;
  font-family: 'Manrope', sans-serif;
  text-align: left;
  flex: 1;
  letter-spacing: -0.01em;
}
</style> 