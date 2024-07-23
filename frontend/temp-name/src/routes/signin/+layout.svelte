<script lang="ts">
    import Navbar from "../../static/Navbar.svelte";
	import { afterUpdate, onMount } from "svelte";
    import { page } from "$app/stores";
	import { afterNavigate, goto } from "$app/navigation";
    import { AuthStore } from "../../data-store";
</script>

<Navbar></Navbar>
<div class="slotter">
    <slot />
</div>

<style>
    .slotter {
        display: flex;
        flex-direction: column;
        flex: 1;
        justify-content: center;
        align-items: center;
        height:100%;
        background-color: #171717;
    }
</style>

