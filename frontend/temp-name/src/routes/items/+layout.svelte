<script lang="ts">
    import Navbar from "../../static/Navbar.svelte";
	import { afterUpdate, onMount } from "svelte";
    import { page } from "$app/stores";
	import { afterNavigate, goto } from "$app/navigation";
    import { AuthStore } from "../../data-store";
    // onMount(() => {
    //     let token = $AuthStore
    //     console.log("token:", token)
    //     console.log("currently in:", $page.url.pathname)
    //     if (token != "no-token" && token != undefined){
    //         return
    //         // add requests for user's database
    //     }
    //     else if ($page.url.pathname != "/signin" &&
    //              $page.url.pathname != "/signup"){
    //         goto("/")
    //     }
    // })
</script>

<Navbar></Navbar>
<div class="slotter">
    <slot />
</div>

<style>
    .slotter {
        display: flex;
        flex: 1;
        justify-content: center;
        align-items: center;
        height:100%;
        background-color: #171717;
    }
</style>

