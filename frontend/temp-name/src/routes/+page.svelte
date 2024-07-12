<script lang="ts">
	import { onMount } from "svelte";
    import { AuthStore } from "../data-store";
    import Paper, {Subtitle, Title} from "@smui/paper";
	import { goto } from "$app/navigation";
    onMount(()=>{
        let authdata = $AuthStore
        if (authdata != "no-token" && authdata != null){
            goto("/home")
        }
    })
</script>


<div class="homepage">
    <Paper unelevated>
        <Title>
            <h1>Welcome to StudyBoost!</h1>
        </Title>
        <Subtitle>
            <p><a href="/signup">Create an account</a> or <a href="/signin">sign in</a> to proceed.</p>
        </Subtitle>
    </Paper>
</div>
