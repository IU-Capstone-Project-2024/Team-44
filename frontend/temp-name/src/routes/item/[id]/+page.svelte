<script lang="ts">
	import TabBar from '@smui/tab-bar';
    import Tab, { Label } from '@smui/tab';
    import Paper, { Content, Subtitle, Title } from '@smui/paper';
	import { QuizStore, SummaryStore, TextStore } from '../../../data-store.js';
	import QuizPage from '../../../static/QuizPage.svelte';
    let active = "Text"
    let title = $TextStore[0]
    let text = $TextStore[1]
    let summary = $SummaryStore.summary[0]
    let quiz = $QuizStore
    let questNum = 0
    console.log("Stored object:", $QuizStore)
</script>
<div>
    <TabBar tabs={["Text", "Summary", "Quiz"]} let:tab bind:active>
        <Tab {tab}>
            <Label>{tab}</Label>
        </Tab>  
    </TabBar>
    <div class="center-content">
        {#if active == "Text"}
        <Paper variant="unelevated">
            <Content>
                <Title>{title}</Title>
                <Subtitle>{text}</Subtitle>
            </Content>
        </Paper>
        {:else if active == "Summary"}
        <Paper variant="unelevated">
            <Content>
                <Title>{title}</Title>
                <Subtitle>{summary}</Subtitle>
            </Content>
        </Paper>
        {:else if active == "Quiz"}
        <QuizPage quiz={quiz} />
        {/if}
    </div>
</div>

<style>
    /* .center-content {
        position: fixed;
    } */
</style>