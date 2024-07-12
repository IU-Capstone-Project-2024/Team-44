<script lang="ts">
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

    onMount(()=>{
        let authdata = $AuthStore
        if (authdata == "no-token" || authdata == null){
            goto("/")
        }
    })
</script>

<div class="mainArea" style="display: flex;">
    <Drawer>
        <Item></Item>
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
    <div style="height: 100%; width:100%;align-items:stretch">
        <AppContent class="app-content" >
            <Paper square variant="unelevated" >
                <Title>
                    <Text>Homepage</Text>
                </Title>
                <br />
                <Content>
                    <pre class="status">{currentTab}</pre>
                </Content>

            </Paper>
        
        </AppContent>
    </div>
</div>




<style>
    .mainArea {
        height: 90vh;
        display: flex;
        flex-direction: row;

    }
   
</style>
