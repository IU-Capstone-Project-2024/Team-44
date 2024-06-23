<script lang="ts">
    let links = [{text: "Home", link: "/home"}, {text: "About", link: "/about"}, {text: "Contacts", link: "/contacts"}]
</script>



<header>
    <div class="title">
        <p class="title-text">Title</p>
    </div>
    <div class="links">
        {#each links as {text, link}, index(text)}
        <a href="{link}"><p>{text}</p></a>
        {/each}
        <div class="sign-in">
            <a href="/signup">Sign up</a>
        </div>
    </div>
</header>

<style>
    header {
        height: min(10vh, 100);
        display: flex;
        flex-direction: row;
        background-color: aquamarine;
        padding: 0;
        margin: 0;
    }

    .title {
        background-color: rgb(140, 140, 255);
        min-width: 15vw;
        text-align: center;
        flex: 15;
    }

    .title-text {
        color: white;
    }

    .links {
        background: azure;
        display: flex;
        flex-direction: row;
        flex: 75;
    }
    a {
        flex: 25;
        justify-content: center;
        align-items: center;
        min-width: 10vw;
        background-color: aquamarine;
        color: white;
        border: 1 dotted red;
    }
    .sign-in {
        flex: 25;
        justify-content: center;
        align-items: center;
        min-width: 10vw;
        background-color: aquamarine;
        color: white;
        border: 1 dotted red;
    }
    p {
        text-align: center;
    }
    a:hover{
        opacity: 50%;
    }
</style>
