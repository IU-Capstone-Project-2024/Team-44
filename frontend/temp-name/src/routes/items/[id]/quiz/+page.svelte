<script lang="ts">
    import { onMount } from "svelte";
    import { AuthStore } from "../../../../data-store";
    import { goto } from "$app/navigation";
    import { page } from "$app/stores";
    import { QuizStore, TextStore} from "../../../../data-store";
    import QuizPage from "../../../../static/QuizPage.svelte";
	import Button, { Label } from "@smui/button";
	import Checkbox from "@smui/checkbox";
	import FormField from "@smui/form-field";

    let token = $AuthStore
	let myHeader = new Headers();
    myHeader.append("Authorization", `Token ${token}`)
	const quizEndpoint = "https://study-boost.ru/quiz/"
    let quizStore = $QuizStore
    let text = $TextStore[1]
    let quizLoaded = false
    let useDB = false
    let sample = {
            question: "Sample Question",
            options: ["ans1", "ans2", "ans3", "ans4"],
            correct_answers: ["ans1"],
    }

    onMount(() => {
            QuizStore.set({questions: [sample]})
            let token = $AuthStore
            console.log("token:", token)
            if (quizStore.questions.length == 1 && quizStore.questions[0] == sample){
                goto("/send")
            }
            // else if (token == "no-token" || token == undefined){
            //     goto("/")
            // }
        }
    )
    
    let removesample = () =>{
        QuizStore.update(prev => {
				let questionList = prev.questions
				questionList = questionList.slice(1)
				prev.questions = questionList
				return prev
			})
		console.log("QuizStore state:", $QuizStore);
    }

    let updateQuiz = (question) => {
		QuizStore.update(prev => {
				let questionList = prev.questions
				questionList.push(question)
				prev.questions = questionList
				return prev
			})
		console.log("QuizStore state:", $QuizStore);	
	}

    
    
    async function readQuizData() {
		let sendQuizData = new FormData()
		sendQuizData.append("text", text)
        sendQuizData.append("useDB", useDB.toString())
		const response = await fetch(quizEndpoint, {
			method: "POST",
			body: sendQuizData,
			headers: myHeader
		})
		.catch(error => {
			console.log("error:", error)
			alert(error)
			return new Response()
		})

		for await (const chunk of response.body){
			let message = new TextDecoder().decode(chunk);
			message = message.replace(/data: /g, "")
			message = message.replace(/'/g, '"')
			console.log("recieved a message:", message)
			if (message != "done"){
				let appendix = JSON.parse(message)
				appendix = appendix.questions[0]
				console.log("to be appended:", appendix)
				updateQuiz(appendix)
			}
		}
		console.log("done")
        removesample();
        quizLoaded = true
	}
    
    
</script>

{#if !quizLoaded}
    <div style="display: flex; flex-direction:column; ">

        
        <Button on:click={readQuizData} variant="unelevated"><Label>
            <div class="mdc-typography--headline4">
            generate the quiz!
            </div>
        </Label></Button>
        <div style="display:flex; flex-direction:row; justify-content:center">
            <FormField>
                <Checkbox bind:value={useDB}/>
                <div class="mdc-typography--subtitle1">
                    Use database?
                </div>
            </FormField>
        </div>
    </div>
{:else} 
    <QuizPage quiz={$QuizStore} />
{/if}