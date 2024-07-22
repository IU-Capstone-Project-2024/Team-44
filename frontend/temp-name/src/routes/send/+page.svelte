<script lang="ts">
	import { goto } from "$app/navigation";
	import { page } from "$app/stores";
	import { onMount } from "svelte";
	import Paper, {Title} from "@smui/paper";
	import Checkbox from '@smui/checkbox';
	import FormField from '@smui/form-field';
	import Button, { Label } from "@smui/button";
	import Textfield, { Textarea } from "@smui/textfield";
	import { AuthStore, QuizStore, SummaryStore, TextStore } from "../../data-store";
	import CircularProgress from '@smui/circular-progress'; 
	import CharacterCounter from '@smui/textfield/character-counter';
	import { json } from "@sveltejs/kit";
	let token = $AuthStore
	let myHeader = new Headers();
    myHeader.append("Authorization", `Token ${token}`)
	const quizEndpoint = "https://study-boost.ru/quiz/"
	const summEndpoint = "https://study-boost.ru/summary/"

    // onMount(() => {
    //     let token = $AuthStore
    //     console.log("token:", token)
    //     console.log("currently in:", $page.url.pathname)
    //     if (token != "no-token" && token != undefined){
    //         return
    //         // add requests for user's database
    //     }
    //     else {
    //         goto("/")
    //     }
    // })

	let updateQuiz = (question: any) => {
		QuizStore.update(prev => {
				let questionList = prev.questions
				questionList.push(question)
				prev.questions = questionList
				return prev
			})
		console.log("QuizStore state:", $QuizStore);	
	}

	
    let doQuiz = true
    let doSum = true
	let docTitle = ""
    let docText = ""
	let sent = false
	let quizLoaded = false
	let summLoaded = false

	async function readQuizData() {
		let sendQuizData = new FormData()
			sendQuizData.append("text", docText)
			const response = await fetch(quizEndpoint, {
				method: "POST",
				body: sendQuizData,
				headers: myHeader
			})
			.catch(error => {
				console.log("error:", error)
				alert(error)
				sent = false
			})
			for await (const chunk of response.body){
				let message = new TextDecoder().decode(chunk);
				message = message.slice(6)
				message = message.replace(/'/g, '"')
				console.log("recieved a message:", message)
				let appendix = JSON.parse(message)
				appendix = appendix.questions[0]
				console.log("to be appended:", appendix)
				updateQuiz(appendix)
			}
			sent = false
			console.log("done")
			goto("/items/1/quiz")
	}

    let handleSend = (() => {
		sent = true
		

		TextStore.set([docTitle, docText])
		if (doQuiz) {
			readQuizData()
		}
		if (doSum) {
			let sendSummData = new FormData()
			sendSummData.append("query", docText)
			fetch(summEndpoint, {
				method: "POST",
				body: sendSummData,
				headers: myHeader
			})
			.then(response => response.json())
			.then(data => {
				summLoaded = true
				console.log(data)
				SummaryStore.set(data)
			})
			.catch(error => {
				console.log("error:", error)
				alert(error)
				sent = false
			})
		}
		
		
    })

</script>

<form>
	<Paper square variant="unelevated">
		<div style="display:flex; flex-direction:column; justify-content:center">
			<Title>Add a text to summarize:</Title>
			<Textfield textarea
			label="Enter the title..." 
			bind:value={docTitle} />
			<Textfield textarea
			label="Enter your text..." 
			input$maxlength={10000}
			bind:value={docText}>
			<CharacterCounter slot="helper">0 / 10000</CharacterCounter>
			</Textfield>
			<br />
			<FormField>
				<Checkbox bind:checked={doQuiz} /><span>quiz</span>
			</FormField>
			<FormField>
				<Checkbox bind:checked={doSum} /><span>summary</span> 
			</FormField>
			<br />	
			<Button variant="raised" disabled={sent} on:click={handleSend}>
				<Label>
					Send to summarize!{#if sent}<CircularProgress style="height: 10px; width: 10px;" indeterminate />{/if}
				</Label>
			</Button>
			
			{#if quizLoaded && summLoaded}
				<a href="/items/1"><span>Go to the item</span></a>
			{/if}
		</div>
	</Paper>
</form>