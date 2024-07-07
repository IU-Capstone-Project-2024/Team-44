<script lang="ts">
	import TabBar from '@smui/tab-bar';
    import Tab, { Label } from '@smui/tab';
    import Paper, { Content } from '@smui/paper';
	import { DataStore } from '../../../data-store.js';
	import QuizPage from '../../../static/QuizPage.svelte';
    export let data;
    let active = "Text"
    let stored : any = $DataStore
    let text = stored.text
    let summary = stored.summary
    let quiz = stored.quiz
    let questNum = 0
    console.log("Stored object:", stored)
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
    <QuizPage
    question={quiz.quests[questNum].question} 
    options={quiz.quests[questNum].options} 
    answer={quiz.quests[questNum].answer} 
    />
    {/if}


    <h1>This is Document#{data.id}</h1>
</div>