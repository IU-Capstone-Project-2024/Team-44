<script lang="ts">
    import { Input } from '@smui/textfield';
    import Fab from '@smui/fab';
    import { Icon } from '@smui/common';
    import TopAppBar, {Row, Section, Title, } from "@smui/top-app-bar"
    import Paper from '@smui/paper';
    import { AuthStore } from '../data-store';

    let links = [{text: "Sign up", link: "/signup"}, {text: "Sign out", link: "/signout"}]
    let prominent = false
    let dense = false
    let value = ""
    
    function handleKeyDown(event: CustomEvent | KeyboardEvent) {
        event = event as KeyboardEvent;
        if (event.key === 'Enter') {
            doSearch();
        }
    }
    function doSearch() {
        alert('Search for ' + value)
        value = ""
    }

    let token = $AuthStore
    let authed = false
    if (token != "no-token" && token != undefined){
        authed = true
    }
</script>



<TopAppBar variant="static" {prominent} {dense} color="primary">
    <Row>
        <div class="title">
            <Section>
                <Title><a href="/home" style="text-decoration: none;">StudyBoost ⚡</a></Title>
            </Section>

        </div>
        <Section>

        <div class="solo-demo-container solo-container">
            <Paper class="solo-paper" elevation={6}>
                <Icon class="material-icons">search</Icon>
                <Input
                  bind:value
                  on:keydown={handleKeyDown}
                  placeholder="Search"
                  class="solo-input"
                />
            </Paper>
            <Fab
                on:click={doSearch}
                disabled={value === ''}
                color="primary"
                mini
                class="solo-fab"
                >
                <Icon class="material-icons">arrow_forward</Icon>
            </Fab>
        </div>
                    
        </Section>
        <Section align="end">
            <Title>
                {#if authed == false}
                    <a href="/signin" style="text-decoration: none;"><p>Sign in</p></a>
                {:else}
                    <a href="/signout" style="text-decoration: none;"><p>Sign out</p></a>
                {/if}
            </Title>
        </Section>
    </Row>

</TopAppBar>

<style>
    .title {
        display: contents;
        width: auto;
        max-width: 15vw;
    }
    
    .solo-container {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    * :global(.solo-paper) {
        display: flex;
        align-items: center;
        flex-grow: 1;
        width: auto;
        margin: 0 12px;
        padding: 0 12px;
    }
    * :global(.solo-paper > *) {
        display: inline-block;
        margin: 0 12px;
    }
    * :global(.solo-input) {
        flex-grow: 1;
        color: var(--mdc-theme-on-surface, #fff);
    }
    * :global(.solo-input::placeholder) {
        color: var(--mdc-theme-on-surface, #fff);
        opacity: 0.6;
    }
    * :global(.solo-fab) {
        flex-shrink: 0;
    }
     a {
        flex: 25;
        justify-content: center;
        align-items: center;
        min-width: 10vw;
        color: white;
    }
    a:hover{
        opacity: 50%;
    }
</style>
