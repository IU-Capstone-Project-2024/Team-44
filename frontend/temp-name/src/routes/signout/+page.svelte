<script lang="ts">
	import { onMount } from "svelte";
	import { AuthStore } from "../../data-store";
	import { goto } from "$app/navigation";
    let token = $AuthStore
    let myHeader = new Headers();
    myHeader.append("Authorization", `Token ${token}`)

    onMount(() => {
        console.log(myHeader.values());
        const endpoint = "https://study-boost.ru/authentication/api/signout/"
        fetch(endpoint, {method: 'GET', headers: myHeader})
        .then(response => {
            AuthStore.set("no-token")
            console.log("signout complete")
            goto("/signin")
        }).catch(
            error => {
                console.log(error)
                alert(error)
            }
        )
        
    })
</script>