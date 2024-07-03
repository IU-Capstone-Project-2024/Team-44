<script lang="ts">
	import { goto } from "$app/navigation";

    let options = ["Notes and Summaries", "Planner", "Quizzes"]
    let handleAdd = (() => {
        goto("/send")
    })
</script>

<div class="leftBar">

    <div class="open-file">
        <button class="open-file-button" on:click={handleAdd}>+ Add</button>
    </div>
    <div class="options">
        {#each options as optText}
        <button class="opt">{optText}</button>
        {/each}
    </div>
    
</div>
<style>
    .leftBar {
        display: flex;
        flex: 15;
        flex-direction: column;
        background-color: antiquewhite;
        border: 1px solid black;
    }

    .open-file {
        display: flex;
        justify-content: center;
    }

    .options {
        display: flex;
        flex-direction: column;
    }

    .opt {
        margin-top: 10px;
        margin-bottom: 10px;
        background-color: rgb(13, 255, 174);
        
    }
</style>