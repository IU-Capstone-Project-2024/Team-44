<script lang="ts">
    import TopAppBar, {Row, Section, Title, } from "@smui/top-app-bar"
    let links = [{text: "Sign up", link: "/signup"}, {text: "Sign out", link: "/signout"}]
    let prominent = false
    let dense = false
</script>



<TopAppBar variant="static" {prominent} {dense} color="primary">
    <Row>
        <Section>
            <Title>StudyBoost ⚡</Title>
        </Section>
        <Section align="start">
            <Title><a href="/home" >Home</a></Title>
        </Section>
        <Section align="end">
            {#each links as {text, link}}
            <Title><a href="{link}"><p>{text}</p></a></Title>
            {/each}
        </Section>
    </Row>

</TopAppBar>

<style>
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
