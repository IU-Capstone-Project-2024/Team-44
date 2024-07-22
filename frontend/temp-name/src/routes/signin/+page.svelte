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

<Paper square >
    
    <Title>Sign in</Title>
    <form class="signin-card" on:submit={handleSubmit}>
        <FormField>
            <Textfield bind:value={username} label="username">
                <!-- <HelperText slot="helper">username</HelperText> -->
            </Textfield>
        </FormField>
        <br>
        <FormField>
            <Textfield bind:value={password} label="password">
            </Textfield>
        </FormField>
        <br>
        <br>
        <Button variant="raised" disabled={clicked}>Sign in</Button>
        <br>
    </form>
    <span>Don't have an account? <a href="/signup">Sign up</a></span>
    {#if showInvalidForm}
        <h4 class="color:red">Form data is not valid!</h4>
    {/if}
    {#if signinSuccess}
        <h4 class="color: green">Sign in successful!</h4>
        <p>Go to <a href="/home">home</a>. </p>
    {/if}
</Paper>