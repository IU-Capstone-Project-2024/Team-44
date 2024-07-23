<script lang="ts">
	import FormField from '@smui/form-field';
	import Button from "@smui/button";
    import Dialog, { Title, Content, Actions } from '@smui/dialog';
	import Textfield from "@smui/textfield";
    let username = ""
    let email = ""
    let first_name = ""
    let last_name = ""
    let telegram_id = ""
    let password = ""
    let repeat_password = ""
    let showInvalidForm = false
    let signupError = false
    let signupSuccess = false
    
    let validFields = () => {
        return username.length > 0 
        && email.length > 0 
        && telegram_id[0] == "@"
        && first_name.length > 0
        && last_name.length > 0
        && password.length > 0
        && repeat_password == password
    }

    let handleSubmit = () => {
        if (!validFields()){
            showInvalidForm = true;
            return
        }
        const endpoint = "https://study-boost.ru/authentication/api/signup/"
        let sendData = new FormData()
        sendData.append("username", username)
        sendData.append("email", email)
        sendData.append("first_name", first_name)
        sendData.append("last_name", last_name)
        sendData.append("telegram_id", telegram_id)
        sendData.append("password", password)
        fetch(endpoint, {method: 'POST', body: sendData}).then(response => response.json()).then(
        ).catch(error => signupError = true)
        if (!signupError) signupSuccess = true
    }
</script>
<div class="signup-container">
    {#if !signupSuccess || signupError}
        
    
    <div class="signup">
        <div class="mdc-typography--headline4">Sign up</div>
    </div>
    <div class="main-container">
        <form class="signup-card" on:submit={handleSubmit}>
            <FormField>
                <Textfield bind:value={username} label="username" />
            </FormField>
            <br>
            <FormField>
                <Textfield bind:value={email} label="e-mail" />
            </FormField>
            <br>
            <FormField>
                <Textfield bind:value={telegram_id} label="telegram id" />
            </FormField>
            <br>
            <FormField>
                <Textfield bind:value={first_name} label="first name" />
            </FormField>
            <br>
            <FormField>
                <Textfield bind:value={last_name} label="last name" />
            </FormField>
            <br>
            <FormField>
                <Textfield bind:value={password} type="password" label="password" />
            </FormField>
            <br>
            <FormField>
                <Textfield bind:value={repeat_password} type="password" label="repeat password" />
            </FormField>
            <br>
            <br>
            <Button variant="raised">Sign up</Button>
            <br>
        </form>
    </div>
    <div style="display:flex; justify-content:center">
        <div class="mdc-typography--subtitle1">Already have an account? <a href="/signin">Sign in</a></div> 
    </div>
    {#if showInvalidForm}
        <div class="mdc-typography--headline6">Form data is not valid!</div>
    {/if}
    {#if signupError}
    <div class="mdc-typography--headline6">Server error</div>
    {/if}
    {:else}
    <div class="success-container">
        <div class="mdc-typography--headline4">Sign up successful!</div>
        <div class="mdc-typography--headline6">
            We have sent you an e-mail with a verification link.<br>
            Please click the link to verify your account.
        </div>
    </div>

{/if}
</div>

<style>
    .signup-container {
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

    .signup {
        display: flex;
        justify-content: center;
        padding: 10px 7%;
    }

    .signup-card {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .success-container {
        display: flex;
        flex-direction: column;
        justify-content:space-evenly;
        height: min(max(80%, 300px), 400px);
        width: min(max(80%, 300px), 600px);
    }
</style>