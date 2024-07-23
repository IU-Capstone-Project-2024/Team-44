<script>
    import { onMount } from "svelte";
    import { AuthStore } from "../../data-store";
    import { page } from "$app/stores";
    import { goto } from "$app/navigation";

    
    onMount(() => {
        goto("/")
    })
</script>