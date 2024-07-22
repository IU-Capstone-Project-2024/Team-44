<script lang="ts">
	import { onMount } from "svelte";
	import { page } from "$app/stores";
	import { goto } from "$app/navigation";
	import Radio from "@smui/radio";
	import Checkbox from '@smui/checkbox';
	import FormField from '@smui/form-field';
	import Button, { Label } from "@smui/button";
	import Textfield from "@smui/textfield";
	import { AuthStore, SummaryStore, TextStore } from "../../data-store";
	import CircularProgress from '@smui/circular-progress'; 
	import CharacterCounter from '@smui/textfield/character-counter';
	let token = $AuthStore
	let myHeader = new Headers();
    myHeader.append("Authorization", `Token ${token}`)
	const quizEndpoint = "https://study-boost.ru/quiz/"
	const summEndpoint = "https://study-boost.ru/summary/"

    onMount(() => {
        let token = $AuthStore
        console.log("token:", token)
        console.log("currently in:", $page.url.pathname)
        if (token != "no-token" && token != undefined){
            return
            // add requests for user's database
        }
        else {
            goto("/")
        }
    })
	
    let toDo = "quiz" 
	let docTitle = ""
    let docText = ""
	let sent = false
	let quizLoaded = false
	let summLoaded = false

    let handleSend = (() => {
		sent = true
		TextStore.set([docTitle, docText])
		if (toDo == "quiz") {
			goto("/items/1/quiz")
		}
		else {
			let sendSummData = new FormData()
			sendSummData.append("text", docText)
			fetch(summEndpoint, {
				method: "POST",
				body: sendSummData,
				headers: myHeader
			})
			.then(response => response.json())
			.then(data => {
				if (data.summary==0)
				summLoaded = true
				console.log(data)
				SummaryStore.set(data)
				goto("/items/1/")
			})
			.catch(error => {
				console.log("error:", error)
				alert(error)
				sent = false
			})
		}	
    })

</script>

<div class="send-container">
	<div class="form-container">
		<div class="form-title">
			<div class="mdc-typography--headline4">
				Add a text to process:
			</div>
		</div>
		<div class="fields">
			<Textfield label="Enter the title..." bind:value={docTitle} />
			<hr >
			<Textfield textarea
			label="Enter your text..." 
			input$maxlength={10000}
			bind:value={docText}
			input$rows={10}>
			<CharacterCounter slot="helper">0 / 10000</CharacterCounter>
			</Textfield>
			<FormField>
				<Radio bind:group={toDo} value="quiz" color="secondary"/>
				<div class="mdc-typography--subtitle1">quiz</div>
			</FormField>
			<FormField>
				<Radio bind:group={toDo} value="summ" color="secondary"/>
				<div class="mdc-typography--subtitle1">summary</div>
			</FormField>
		</div>
	
	</div>
	<Button variant="raised" disabled={sent} on:click={handleSend}>
		<Label>
			{#if toDo == "quiz"}
				Make a quiz!
			{:else}
				Summarize!
			{/if}
			{#if sent}<CircularProgress style="height: 10px; width: 10px;" indeterminate />{/if}
		</Label>
	</Button>
	
	{#if quizLoaded && summLoaded}
		<a href="/items/1"><span>Go to the item</span></a>
	{/if}
</div>
<style>
	hr {
		width: 100%;
		color: rgba(0, 0, 0, 0);
	}
	.send-container {
		display: flex;
		flex-direction: column;
		justify-content:space-evenly;
		height: min(max(80%, 300px), 600px);
		width: min(max(80%, 500px), 1500px);
	}

	.form-container{
		padding: 10px;
        background-color: #333;
        display:flex;
        justify-content:space-between;
        flex-direction:column;
        border: 1px solid #ff3e00;
        border-radius: 10px;

	}
	.form-title {
		display: flex;
        justify-content: center;
        padding: 10px 7%;
		flex:1;
	}
	.fields {
		flex:1;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
	}

</style>