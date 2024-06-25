<script lang="ts">
    import { AuthStore } from "../../data-store";
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
{#if showInvalidForm}
    <h4 class="color:red">Form data is not valid!</h4>
{/if}
{#if signupError}
    <h4 class="color:red">Server error</h4>
{/if}
<form class="login-card" on:submit={handleSubmit}>
    <div class="fieldiv">
        <input type="text" bind:value={username} placeholder="username">
    </div>
    <div class="fieldiv">
        <input type="email" bind:value={email} placeholder="you@example.com">
    </div>
    <div class="fieldiv">
        <input type="text" bind:value={telegram_id} placeholder="@you">
    </div>
    <div class="fieldiv">
        <input type="text" bind:value={first_name} placeholder="Ivan">
    </div>
    <div class="fieldiv">
        <input type="text" bind:value={last_name} placeholder="Ivanov">
    </div>
    <div class="fieldiv">
        <input type="password" bind:value={password} placeholder="password">
    </div>
    <div class="fieldiv">
        <input type="password" bind:value={repeat_password} placeholder="repeat password">
    </div>

    <button type="submit">Sign up</button>
</form>
{#if signupSuccess && !signupError}
    <h4 class="color: green">Sign up successful!</h4>
    <p>Go to <a href="/signin">sign in</a>. </p>
{/if}
<p>Already have an account? <a href="/signin">Sign in</a></p>