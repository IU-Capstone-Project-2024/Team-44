<script>
    import { onMount } from "svelte";
    import { AuthStore } from "../../data-store";
    import { page } from "$app/stores";
    import { goto } from "$app/navigation";

    
    onMount(() => {
        let token = $AuthStore
        console.log("token:", token)
        console.log("currently in:", $page.url.pathname)
        if (token != "no-token" && token != undefined){
            return
            // add requests for user's database
        }
        else {
            goto("/")
        }
    })
</script>