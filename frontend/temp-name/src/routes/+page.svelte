<script lang="ts">
	import { onMount } from "svelte";
    import { AuthStore } from "../data-store";
    import Paper, {Subtitle, Title} from "@smui/paper";
	import { goto } from "$app/navigation";
    import Navbar from "../static/Navbar.svelte";
    onMount(()=>{
        let authdata = $AuthStore
        if (authdata != "no-token" && authdata != null){
            goto("/home")
        }
    })
</script>


<Navbar></Navbar>
<div class="slotter">
    <Paper unelevated>
        <div class="homepage">
            <Title>
                <h1>Welcome to StudyBoost!</h1>
            </Title>
            <Subtitle>
                <p><a href="/signup">Create an account</a> or <a href="/signin">sign in</a> to proceed.</p>
            </Subtitle>
        </div>
    </Paper>
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

    .homepage {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
</style>