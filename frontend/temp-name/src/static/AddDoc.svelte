<script lang="ts">
	import { goto } from "$app/navigation";
    import { DataStore } from "../data-store";
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
        fetch(endpoint, {method: "POST", body: sendData})
        .then(response => response.json())
        .then(data => goto("/item/1"))
    })

</script>

<form>
    <h4>Add a text to summarize:</h4>
    <textarea placeholder="Enter your text..." bind:value={docText}></textarea>
    <br />
    <p><input type="checkbox" bind:checked={doQuiz} /> quiz </p>
    <p><input type="checkbox" bind:checked={doSum} /> summary </p>
    <p><input type="checkbox" bind:checked={useRAG} /> Use RAG? </p>
    <button on:click={handleSend}>Send to summarize!</button>
</form>