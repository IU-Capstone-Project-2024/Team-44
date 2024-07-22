<script lang="ts">
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';
    import { AuthStore } from '../../../data-store.js';
    import Paper, { Content, Subtitle, Title } from '@smui/paper';
	import { QuizStore, SummaryStore, TextStore } from '../../../data-store.js';
	import Fab, {Icon, Label} from '@smui/fab';
    export let data;
    let active: string = "Text"
    let inactive: string = "Summary";
    let title = $TextStore[0]
    let text = $TextStore[1]
    let summary = $SummaryStore.summary[0]
    let density = new Map ([["Text", "auto_stories"], ["Summary", "article"]])
    let quiz = $QuizStore
    console.log("Stored object:", $QuizStore)

    let switchText = (()=>{
        if (active == "Summary") {
            active = "Text"
            inactive = "Summary"
        }
        else {
            active = "Summary"
            inactive = "Text"
        }
            
    })

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
<div class="flexy">
    <Paper variant="unelevated">
    {#if active == "Text"}
        <Content>
            <Title>{title}</Title>
            <Subtitle>{text}</Subtitle>
        </Content>

    {:else if active == "Summary"}
        <Content>
            <Title>{title}</Title>
            <Subtitle>{summary}</Subtitle>
        </Content>
    {/if}
    <div class="margins">
        <Fab color="secondary" on:click={switchText} extended ripple={false}>
            <Label>Show {inactive}</Label>
            <Icon class="material-icons">{density.get(inactive)}</Icon>
        </Fab>
        <Fab color="primary" on:click={()=>{goto(`/items/${data.id}/quiz`)}} extended ripple={false}>
            <Label>Go to quiz</Label>
            <Icon class="material-icons">checklist</Icon>
        </Fab>
    </div>
    </Paper>
</div>

<style>
    .margins {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
    }
</style>