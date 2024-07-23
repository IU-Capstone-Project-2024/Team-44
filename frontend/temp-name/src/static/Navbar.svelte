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



<TopAppBar variant="fixed" {prominent} {dense} color="primary">
    <div class="bg-gradient">
        <Row>
            <Section>
                <div class="title">

                    <Title><a href="/" style="text-decoration: none;">StudyBoost ⚡</a></Title>
                </div>
                
            </Section>

            <Section align="end">
                <div class="title">
                    <Title><a href="/send" style="text-decoration: none;">Send</a></Title>                
                </div>
                <div class="title">
                    <Title><a href="/about" style="text-decoration: none;">About</a></Title>                
                </div>
                <Title>
                    {#if authed == false}
                        <a href="/signin" style="text-decoration: none;"><p>Sign in</p></a>
                    {:else}
                        <a href="/signout" style="text-decoration: none;"><p>Sign out</p></a>
                    {/if}
                </Title>
            </Section>
        </Row>
    </div>

</TopAppBar>

<style>
    .title {
        display: contents;
        width: auto;
        max-width: 15vw;
    }
    .bg-gradient{
        display: flex;
        background: linear-gradient(270deg, rgba(22,22,22,1) 0%, rgba(255,62,0,1) 100%);
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
