<script lang="ts">
	import { goto } from "$app/navigation";
    import Paper, {Subtitle, Title} from "@smui/paper";
	import Checkbox from '@smui/checkbox';
	import FormField from '@smui/form-field';
	import Button, { Label } from "@smui/button";
    import { Text } from "@smui/list";
	import Textfield from "@smui/textfield";
    import HelperText from '@smui/textfield/helper-text';
    export let quiz : any = {}
    console.log(quiz)
    let questNum : number = 0
    let question : string = quiz.questions[questNum].question
    let options : Array<string> = quiz.questions[questNum].options
    let answer : Array<string> = quiz.questions[questNum].correct_answers
    console.log(question)
    console.log(options)
    console.log(answer)
    let selected : Array<string> = []
    let result : string = ""
    let checked = false
    let checkAnswers = (() => {
        if (answer.length != selected.length){
            result = "Incorrect amount of answers!"
            return
        }
        checked = true
        const ans = answer.concat().sort()
        const sel = selected.concat().sort()
        for (let i = 0; i < ans.length; i++){
            if (ans[i] != sel[i]) {
                result = `The answer is not correct, the correct answer is: ${ans}`
                return
            }
        }
        selected = []
        result = "The answer is correct!"
    })
    let nextQuest = (()=>{
        checked = false
        questNum = questNum+1
        question = quiz.questions[questNum].question
        options = quiz.questions[questNum].options
        answer = quiz.questions[questNum].correct_answers
        result = ""
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
        {#each options as opt}
        <FormField>
            <Checkbox bind:group={selected} value={opt} />
            <Subtitle>  
                {opt}
            </Subtitle>
        </FormField>
        <br />
        {/each}
        <br>
        <Button disabled={checked} on:click={checkAnswers} >
            <Label>Check</Label>
        </Button>
        {#if questNum < quiz.questions.length - 1}
        <Button on:click={nextQuest} >
            <Label >Next Question</Label>
        </Button>
        <br>
        {/if}
        <Text>
            {result}
        </Text>
    </Paper>
</div>

