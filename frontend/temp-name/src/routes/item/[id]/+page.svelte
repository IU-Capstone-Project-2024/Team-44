<script lang="ts">
	import TabBar from '@smui/tab-bar';
    import Tab, { Label } from '@smui/tab';
    import Paper, { Content } from '@smui/paper';
	import { goto } from '$app/navigation';
    export let data
    let active = "Text"
    let text = "lorem ipsum dolor res"
    let summary = "lorem dolor"
    let quiz = ""
</script>
<div>
    <TabBar tabs={["Text", "Summary", "Quiz"]} let:tab bind:active>
        <Tab {tab}>
            <Label>{tab}</Label>
        </Tab>  
    </TabBar>    
    {#if active == "Text"}
    <Paper variant="unelevated">
        <Content>
            <h1>{text}</h1>
        </Content>
    </Paper>
    {:else if active == "Summary"}
    <Paper variant="unelevated">
        <Content>
            <h1>{summary}</h1>
        </Content>
    </Paper>
    {:else if active == "Quiz"}
    <h1>There could be a quiz...</h1>
    {/if}


    <h1>This is Document#{data.id}</h1>
</div>