<script lang="ts">
	import { goto } from "$app/navigation";
	import { AuthStore } from "../../data-store";
    import Paper, {Title} from "@smui/paper";
	import FormField from '@smui/form-field';
	import Button from "@smui/button";
	import Textfield from "@smui/textfield";
    let username = ""
    let password = ""
	let showInvalidForm = false
	let signinSuccess = false
    let clicked = false

    let validFields = () => {
        return username.length > 0 
        && password.length > 0
    }

    let handleSubmit = () => {
        clicked = true
        if (!validFields()){
            showInvalidForm = true;
            return
        }
        const endpoint = "https://study-boost.ru/authentication/api/signin/"
        let sendData = new FormData()
        sendData.append("username", username)
		sendData.append("password", password)
        fetch(endpoint, {method: 'POST', body: sendData}).then(response => response.json()).then(data => {
            console.log(data)
            if (data.error != null){
                alert(data.error)
                clicked = false
            }
            else {
                if (data.token){
                    console.log(data.token)
                    AuthStore.update(prev => data.token)
                    signinSuccess = true
                    goto("/home")
                }
                else{
                    alert("Got no token from backend")
                    AuthStore.update(prev => "no-token")
                    if (data.message == "You are logged in"){
                        goto("/send")
                    }
                }
            }
		}).catch(error => {
            alert(error)
			console.log(error)
            clicked = false
		})

    }
</script>

<div class="signin-container">
    <div class="signin">
        <div class="mdc-typography--headline4">Sign in</div>
    </div>
    <div class="main-container">
        <form class="signin-card" on:submit={handleSubmit}>
            <FormField>
                <Textfield bind:value={username} label="username" />
            </FormField>
            <br>
            <FormField>
                <Textfield bind:value={password} type="password" label="password" />
            </FormField>
            <br>
            <br>
            <Button variant="raised" disabled={clicked}>Sign in</Button>
            <br>
        </form>
    </div>
    <div style="display:flex; justify-content:center">
        <div class="mdc-typography--subtitle1">Don't have an account? <a href="/signup">Sign up</a></div> 
    </div>
    {#if showInvalidForm}
        <div class="mdc-typography--headline6">Form data is not valid!</div>
    {/if}
    {#if signinSuccess}
        <div class="mdc-typography--headline6">Sign in successful!</div>
        <p>Go to <a href="/send">sending</a>.</p>
    {/if}
</div>

<style>
    .signin-container {
        display: flex;
        flex-direction: column;
        justify-content:space-evenly;
        height: min(max(80%, 300px), 600px);
        width: min(max(80%, 150px), 300px);
    }

    .main-container {
        padding: 10px;
        background-color: #333;
        display:flex;
        justify-content:center;
        border: 1px solid #ff3e00;
        border-radius: 10px;
    }

    .signin {
        display: flex;
        justify-content: center;
        padding: 10px 7%;
    }

    .signin-card {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
</style>