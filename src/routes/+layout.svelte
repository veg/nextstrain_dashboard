<script lang="ts">
  import '../app.css';
  let { children } = $props();
</script>

<div class="h-screen w-screen overflow-hidden flex flex-col bg-dark-950 text-slate-100 font-sans">
  {@render children()}
</div>
