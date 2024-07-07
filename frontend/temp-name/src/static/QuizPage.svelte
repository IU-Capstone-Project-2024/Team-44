<script lang="ts">
	import { goto } from "$app/navigation";
    import Paper, {Subtitle, Title} from "@smui/paper";
	import Checkbox from '@smui/checkbox';
	import FormField from '@smui/form-field';
	import Button, { Label } from "@smui/button";
    import { Text } from "@smui/list";
	import Textfield from "@smui/textfield";
    import HelperText from '@smui/textfield/helper-text';
    export let questNum : number = 0
    export let question : string = ""
    export let options : Array<string> = []
    export let answer : Array<string> = []
    let selected : Array<string> = []
    let result : string = "nothing yet"
    let checkAnswers = (() => {
        if (answer.length != selected.length){
            result = "answer is not correct: differrent sizes"
            return
        }
        const ans = answer.concat().sort()
        const sel = selected.concat().sort()
        for (let i = 0; i < ans.length; i++){
            if (ans[i] != sel[i]) {
                result = `answer is not correct: ${ans} vs ${sel}`
                return
            }
        }
        result = "answer is correct"
    })
    let nextQuest = (()=>{
        if (result != "answer is correct"){
            result = "Please answer properly before proceding!"
            return
        }
        questNum = questNum+1
    })
</script>

<div class="quiz-container">
    <Paper variant="unelevated">
        {#if question.length == 0}
            <Text>No question was provided</Text>
            <br>
        {/if}
        {#if options.length == 0}
            <Text>No options were provided</Text>
            <br>
        {/if}
        {#if answer.length == 0}
            <Text>No answer was passed</Text>
            <br>
        {/if}
        <Title>{question}</Title>
        {#each options as opt, i}
        <FormField>
            <Checkbox bind:group={selected} value={opt} />
            <Subtitle>  
                {opt}
            </Subtitle>
        </FormField>
        <br />
        {/each}
        <br>
        <Text>
            Now selected: {selected}
        </Text>
        <br>
        <Button on:click={checkAnswers} >
            <Label>Check</Label>
        </Button>
        <Button on:click={()=>0} >
            <Label >Next Question</Label>
        </Button>
        <br>
        <Text>
            {result}
        </Text>
    </Paper>
</div>

