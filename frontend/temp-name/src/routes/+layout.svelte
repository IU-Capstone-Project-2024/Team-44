<script lang="ts">
    import Navbar from "../static/Navbar.svelte";
    import { AuthStore } from "../data-store";
	import { onMount } from "svelte";
    import { page } from "$app/stores";
	import { goto } from "$app/navigation";
    onMount(() => {
        if ($AuthStore != "no-token"){
            return
            // add requests for user's database
        }
        else if ($page.url.pathname != "/signin" &&
                 $page.url.pathname != "/signup"){
            goto("/home")
        }
    })
</script>

<Navbar></Navbar>
<div class="slotter">
    <slot />
</div>

<style>
    .slotter {
        align-items: center;
        height:100%
    }
</style>

