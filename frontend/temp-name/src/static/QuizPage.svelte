<script lang="ts">
    import Paper, {Subtitle, Title} from "@smui/paper";
	import Checkbox from '@smui/checkbox';
	import FormField from '@smui/form-field';
	import Button, { Label } from "@smui/button";
    import { Text } from "@smui/list";
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
        <div style="display:flex; justify-content:center; flex-direction:column; border: 1px solid black">
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
            <div style="display:flex; justify-content:center">
                <Title>{question}</Title>
            </div>
            {#each options as opt}
            <div style="display:flex; justify-content:center">
                <FormField>
                    <Checkbox bind:group={selected} value={opt} />
                    <Subtitle>  
                        {opt}
                    </Subtitle>
                </FormField>
            </div>
            <br />
            {/each}
            <br>
        </div>
        <div style="display:flex; justify-content:center; flex-direction:row">
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
        </div>
    </Paper>
</div>

