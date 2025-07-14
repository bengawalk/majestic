<script lang="ts">
  import LanguageSwitcher from "$lib/components/LanguageSwitcher.svelte";
  import {messages} from "$lib/stores/messages";

  // export let title: string = 'Majestic Bus Station';
</script>

<header class="cupertino-header">
  <h1>{$messages.header()}</h1>
  <div class="language-switcher">
    <LanguageSwitcher />
  </div>
</header>

<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400&display=swap');
.cupertino-header {
  margin-top: 4px;
  margin-bottom: 10px;
  width: 100%;
  display: flex;
  align-items: center;
  z-index: 100;
  position: relative;
  padding-left: 16px;
  padding-right: 16px;
}
.cupertino-header h1 {
  font-size: 22px;
  font-weight: 700;
  color: #222;
  font-family: 'Manrope', sans-serif;
  text-align: left;
  flex: 1;
  letter-spacing: -0.01em;
}
.language-switcher {
  margin-left: auto;
}
</style> 