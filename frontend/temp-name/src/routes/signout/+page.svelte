<script lang="ts">
	import { onMount } from "svelte";
	import { AuthStore } from "../../data-store";
	import { goto } from "$app/navigation";

    onMount(() => {
        const endpoint = "https://study-boost.ru/authentication/api/signout/"
        let nulldata = new FormData()
        nulldata.append("null", "null")
        fetch(endpoint, {method: 'GET'}).then(response => {
            AuthStore.set({})
            console.log("signout complete")
            goto("/signin")
        }).catch(
            error => {
			console.log(error)
            goto("/home")
		})
        
    })
</script>