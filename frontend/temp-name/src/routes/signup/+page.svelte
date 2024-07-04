<script lang="ts">
    import { AuthStore } from "../../data-store";
    import Paper, {Title} from "@smui/paper";
	import FormField from '@smui/form-field';
	import Button from "@smui/button";
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
        const endpoint = "http://localhost:8000/authentication/api/signup/"
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
            <Textfield bind:value={email} label="e-mail">
                <!-- <HelperText slot="helper">e-mail</HelperText> -->
            </Textfield>
        </FormField>
        <br>
        <FormField>
            <Textfield bind:value={telegram_id} label="telegram id">
            </Textfield>
        </FormField>
        <br>
        <FormField>
            <Textfield bind:value={first_name} label="first name">
            </Textfield>
        </FormField>
        <br>
        <FormField>
            <Textfield bind:value={last_name} label="last name">
            </Textfield>
        </FormField>
        <br>
        <FormField>
            <Textfield bind:value={password} label="password">
            </Textfield>
        </FormField>
        <br>
        <FormField>
            <Textfield bind:value={repeat_password} label="repeat password">
            </Textfield>
        </FormField>
        <br>
        <br>
        <Button variant="raised">Sign up</Button>
        <br>
    </form>
    <span>Already have an account? <a href="/signin">Sign in</a></span>
    {#if showInvalidForm}
        <h4 class="color:red">Form data is not valid!</h4>
    {/if}
    {#if signupError}
        <h4 class="color:red">Server error</h4>
    {/if}
    {#if signupSuccess && !signupError}
    <h4 class="color: green">Sign up successful!</h4>
    <p>Go to <a href="/signin">sign in</a>. </p>
{/if}
</Paper>
