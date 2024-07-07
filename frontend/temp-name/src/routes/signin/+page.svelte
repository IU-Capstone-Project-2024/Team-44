<script lang="ts">
	import { goto } from "$app/navigation";
	import { AuthStore } from "../../data-store";
    import Paper, {Title} from "@smui/paper";
	import Checkbox from '@smui/checkbox';
	import FormField from '@smui/form-field';
	import Button from "@smui/button";
	import Textfield from "@smui/textfield";
    import HelperText from '@smui/textfield/helper-text';
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
        const endpoint = "https://study-boost.ru/authentication/api/signin/"
        let sendData = new FormData()
        sendData.append("username", username)
		sendData.append("password", password)
        fetch(endpoint, {method: 'POST', body: sendData}).then(response => response.json()).then(data => {
            console.log(data)
			AuthStore.update(prev => [data])
		}).catch(error => {
            alert(error)
			console.log(error)
		})
        if (!signinError) {
			signinSuccess = true
			goto("/home")
		}
    }
</script>

<Paper square >
    
    <Title>Sign up</Title>
    <form class="signup-card" on:submit={handleSubmit}>
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
        <Button variant="raised">Sign up</Button>
        <br>
    </form>
    <span>Don't have an account? <a href="/signup">Sign up</a></span>
    {#if showInvalidForm}
        <h4 class="color:red">Form data is not valid!</h4>
    {/if}
    {#if signinSuccess && !signinError}
        <h4 class="color: green">Sign up successful!</h4>
        <p>Go to <a href="/signin">sign in</a>. </p>
    {/if}
</Paper>