<script lang="ts">
	import { goto } from "$app/navigation";
	import { AuthStore } from "../../data-store";
    let username = ""
    let password = ""
	let showInvalidForm = false
	let signinError = false
	let signinSuccess = false

    let validFields = () => {
        return username.length > 0 
        && password.length > 0
    }

    let handleSubmit = () => {
        if (!validFields()){
            showInvalidForm = true;
            return
        }
        const endpoint = "http://localhost:8000/authentication/api/signin/"
        let sendData = new FormData()
        sendData.append("username", username)
		sendData.append("password", password)
        fetch(endpoint, {method: 'POST', body: sendData}).then(response => response.json()).then(data => {
			AuthStore.update(prev => [{"username": username}, data])
		}).catch(error => {
			signinError = true
			console.log(error)
		})
        if (!signinError) {
			signinSuccess = true
			goto("/home")
		}
    }
</script>

{#if showInvalidForm}
    <h4 class="color:red">Form data is not valid!</h4>
{/if}
{#if signinError}
    <h4 class="background-color:#F00">Server error</h4>
{/if}
<form class="login-card" on:submit={handleSubmit}>
    <div class="fieldiv">
        <input type="text" bind:value={username} placeholder="username">
    </div>
    <div class="fieldiv">
        <input type="password" bind:value={password} placeholder="password">
    </div>
    <button type="submit">Log in</button>
</form>
<p>Don't have an account? <a href="/signup">Sign up</a></p>
{#if signinSuccess && !signinError}
    <h4 class="color: green">Sign up successful!</h4>
    <p>Go to <a href="/signin">sign in</a>. </p>
{/if}