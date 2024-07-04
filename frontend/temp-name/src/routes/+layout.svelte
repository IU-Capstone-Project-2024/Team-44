<script lang="ts">
    import Navbar from "../static/Navbar.svelte";
    import { AuthStore } from "../data-store";
	import { onMount } from "svelte";
    onMount(() => {
        // add checks for navbar
    })
</script>

<Navbar></Navbar>
<div class="mainbody">
    <slot />
</div>
