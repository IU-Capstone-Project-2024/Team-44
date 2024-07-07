<script lang="ts">
	import { goto } from "$app/navigation";
	import Paper, {Title} from "@smui/paper";
	import Checkbox from '@smui/checkbox';
	import FormField from '@smui/form-field';
	import Button from "@smui/button";
	import Textfield, { Textarea } from "@smui/textfield";
	import { AuthStore, DataStore } from "../../data-store";
	import { get } from "svelte/store"

	let token = $AuthStore
    let doQuiz = false
    let doSum = false
    let useRAG = false
    let docText = ""
    let handleSend = (() => {
        let types = ["text"]
        if (doQuiz) types.push("quiz")
        if (doSum) types.push("sum")
        let options = [docText]
        useRAG ? options.push("RAG") : options.push("noRAG")
        let endpoint = ""
        console.log(docText)
        console.log(`doQuiz = ${doQuiz}`);
        console.log(`doSum = ${doSum}`);
        console.log(`useRAG = ${useRAG}`);
        let sendData = new FormData()
        sendData.append("type", JSON.stringify(types))
        sendData.append("options", JSON.stringify(options))
        fetch(endpoint, {
			headers: {Authorization: `Bearer ${token}`},
			method: "POST",
			body: sendData
		})
        .then(response => response.json())
        .then(data => {
			DataStore.set(data)
			goto("/item/1")
		})
    })

</script>

<form>
	<Paper square variant="unelevated">
		<Title>Add a text to summarize:</Title>
		<Textfield textarea
		label="Enter your text..." 
		input$maxlength={1000}
		bind:value={docText}></Textfield>
		<br />
		<FormField>
			<Checkbox bind:checked={doQuiz} /><span>quiz</span>
		</FormField>
		<FormField>
			<Checkbox bind:checked={doSum} /><span>summary</span> 
		</FormField>
		<FormField>
			<Checkbox bind:checked={useRAG} /><span>Use RAG?</span> 
		</FormField>
		<br>	
		<Button variant="raised" on:click={handleSend}>Send to summarize!</Button>
	</Paper>
</form>