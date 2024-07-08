<script lang="ts">
	import { goto } from "$app/navigation";
	import Paper, {Title} from "@smui/paper";
	import Checkbox from '@smui/checkbox';
	import FormField from '@smui/form-field';
	import Button, { Label } from "@smui/button";
	import Textfield, { Textarea } from "@smui/textfield";
	import { AuthStore, QuizStore, SummaryStore, TextStore } from "../../data-store";
	import CircularProgress from '@smui/circular-progress'; 
	import CharacterCounter from '@smui/textfield/character-counter';
	let token = $AuthStore
    let doQuiz = true
    let doSum = true
    let docText = ""
	let errors = false
	let sent = false
	let quizLoaded = false
	let summLoaded = false
    let handleSend = (() => {
		sent = true

		TextStore.set(docText)
		if (doQuiz) {
			let sendQuizData = new FormData()
			sendQuizData.append("text", docText)
			let endpoint = "https://study-boost.ru/quiz/"
			fetch(endpoint, {
				// headers: {Authorization: `Bearer ${token}`},
				method: "POST",
				body: sendQuizData
			})
			.then(response => response.json())
			.then(data => {
				quizLoaded = true
				console.log(data)
				QuizStore.set(data)
			})
			.catch(error => {
				errors = true
				console.log("error:", error)
			})
		}
		if (doSum) {
			let sendSummData = new FormData()
			sendSummData.append("query", docText)
			let endpoint = "https://study-boost.ru/summary/"
			fetch(endpoint, {
				// headers: {Authorization: `Bearer ${token}`},
				method: "POST",
				body: sendSummData
			})
			.then(response => response.json())
			.then(data => {
				summLoaded = true
				console.log(data)
				SummaryStore.set(data)
			})
			.catch(error => {
				errors = true
				console.log("error:", error)
			})
		}
		
		
    })

</script>

<form>
	<Paper square variant="unelevated">
		<div style="display:flex; flex-direction:column; justify-content:center">
			<Title>Add a text to summarize:</Title>
			<Textfield textarea
			label="Enter your text..." 
			input$maxlength={1000}
			bind:value={docText}>
			<CharacterCounter slot="helper">0 / 1000</CharacterCounter>
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
				<a href="/item/1"><span>Go to the item</span></a>
			{/if}
		</div>
	</Paper>
</form>