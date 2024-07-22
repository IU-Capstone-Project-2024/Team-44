<script lang="ts">
    import { page } from "$app/stores";
    import { goto } from "$app/navigation";
	import { onMount } from "svelte";
    import { AuthStore } from "../../data-store";
    import Drawer, { AppContent, Content, Title } from '@smui/drawer';
    import List, { Item, Text } from '@smui/list';
	import Paper from "@smui/paper";
    import Button, { Icon, Label } from '@smui/button';
    let currentTab = "Welcome!"
    let options = ["Your files", "Planner", "Quizzes"]
    let handleAdd = (() => {
        goto("/send")
    })

    onMount(() => {
        let token = $AuthStore
        console.log("token:", token)
        console.log("currently in:", $page.url.pathname)
        if (token != "no-token" && token != undefined){
            return
            // add requests for user's database
        }
        else {
            goto("/")
        }
    })

</script>

<div class="mainArea" style="display: flex;">
    <Drawer>
        <Item><Text>{currentTab}</Text></Item>
        <Button variant="raised" on:click={handleAdd} ripple={false}>
            <Label>Add a file</Label>
            <Icon class="material-icons">add_circle</Icon>
        </Button>
        <Content>
          <List>
            {#each options as option}
            <Item
            href="javascript:void(0)"
            on:click={() => (currentTab = option)}
            >
            <Text>
                {#if option == "Planner"}
                <s>{option}</s>
                {:else}
                {option}
                {/if}
            </Text>
            </Item>
            {/each}
          </List>
        </Content>
    </Drawer>
    <div style="flex:1;display:flex;justify-content:center;">
        <div class="drawerMain">
            <Title>
                <Text>Homepage</Text>
            </Title>
            <br />
            <Content>
                <pre class="status">{currentTab}</pre>
            </Content>
        </div>
    </div>
</div>




<style>
    .mainArea {
        height: 90vh;
        display: flex;
        flex-direction: row;

    }

    .drawerMain {
        flex:1;
        background-color: var(--mdc-theme-secondary, #333);
    }
   
</style>
