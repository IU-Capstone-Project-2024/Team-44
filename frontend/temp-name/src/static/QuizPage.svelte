<script lang="ts">
    import Dialog, { Title, Content, Actions } from '@smui/dialog';
	import Checkbox from '@smui/checkbox';
	import FormField from '@smui/form-field';
	import Button, { Label } from "@smui/button";
    import { Text } from "@smui/list";
	import { goto } from '$app/navigation';
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
    let size = quiz.questions.length
    let answeredCorrect = 0
    let open = false
    let clicked = "none"

    let checkAnswers = (() => {
        const ans = answer.concat().sort()
        checked = true
        if (answer.length != selected.length){
            result = `The answer is not correct, the correct answer is: ${ans}`
            return
        }
        const sel = selected.concat().sort()
        for (let i = 0; i < ans.length; i++){
            if (ans[i] != sel[i]) {
                result = `The answer is not correct, the correct answer is: ${ans}`
                return
            }
        }
        selected = []
        result = "The answer is correct!"
        answeredCorrect+=1
    })

    let nextQuest = (()=>{
        selected = []
        checked = false
        questNum = questNum+1
        question = quiz.questions[questNum].question
        options = quiz.questions[questNum].options
        answer = quiz.questions[questNum].correct_answers
        result = ""
    })
    let prevQuest = (()=>{
        selected = []
        checked = false
        questNum = questNum-1
        question = quiz.questions[questNum].question
        options = quiz.questions[questNum].options
        answer = quiz.questions[questNum].correct_answers
        result = ""
    })
</script>
{#if open}
<div class="dialog-container">
    <Dialog
    bind:open
    aria-labelledby="simple-title"
    aria-describedby="simple-content"
    >
    <div class="mdc-typography--headline3">Results:</div>
    <div class="mdc-typography--headline5">You have got {answeredCorrect} questions out of {size}.</div>
    <Actions>
        <Button on:click={() => (goto("/send"))}>
        <Label>Ok</Label>
        </Button>
    </Actions>
    </Dialog>
</div>
{:else}
<div class="quiz-container">

    <div class="question-container">
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
        <div class="question">
            <div class="mdc-typography--headline4">
                {question}
            </div>
        </div>
        {#each options as opt, i}
        <div class="option" style={i%2==1?"background-color:#444":"background-color:#333"}>
            <FormField>
                <Checkbox bind:group={selected} value={opt} />
                <div class="mdc-typography--subtitle1">  
                    {opt}
                </div>
            </FormField>
        </div>
        {/each}
    </div>
    <div class="question-container">
        <Button disabled={checked} on:click={checkAnswers} variant="raised" ripple={false}>
            <Label>Check</Label>
        </Button>
        <div class="split-button">
        {#if questNum != 0}
            <Button on:click={prevQuest} ripple={false}>
                <Label >Previous Question</Label>
            </Button>
        {:else}
            <Button on:click={prevQuest} ripple={false} disabled>
                <Label >Previous Question</Label>
            </Button>
        {/if}
        {#if questNum < quiz.questions.length - 1}
            <Button on:click={nextQuest} ripple={false}>
                <Label >Next Question</Label>
            </Button>
        {:else}
            <Button on:click={()=>{open=true}} ripple={false}>
                <Label>Finish quiz</Label>
            </Button>
        {/if}
        </div>
        
    </div>
    <div class="mdc-typography--overline">
        {result}
    </div>

</div>
{/if}

<style>
    .quiz-container {
        display: flex;
        flex-direction: column;
        justify-content:space-evenly;
        height: min(max(80%, 300px), 600px);
        width: min(max(80%, 500px), 1500px);
    }

    .question-container {
        padding: 10px;
        background-color: #333;
        display:flex;
        justify-content:center;
        flex-direction:column;
        border: 1px solid #ff3e00;
        border-radius: 10px;

    }
    .dialog-container {
        padding: 10px;
        background-color: #333;
        display:flex;
        width: 30%;
        height: min(30%, 300);
        flex-direction:column;
        border: 1px solid #ff3e00;
        border-radius: 10px;
    }

    .question {
        display: flex;
        justify-content: center;
        padding: 10px 7%;
    }

    .option {
        display:flex;
        justify-content:start;
        border-radius: 5px;
        padding: 0% 7%;
    }
    .split-button {
        display: flex;
        flex-direction: row;
        justify-content: space-around;
        flex: 1;

    }
</style>
