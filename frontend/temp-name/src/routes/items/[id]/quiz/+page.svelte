<script lang="ts">
    import { onMount } from "svelte";
    import { AuthStore } from "../../../../data-store";
    import { goto } from "$app/navigation";
    import { page } from "$app/stores";
    import { QuizStore } from "../../../../data-store";
    import QuizPage from "../../../../static/QuizPage.svelte";

    let quiz = $QuizStore

    // onMount(() => {
    //     let token = $AuthStore
    //     console.log("token:", token)
    //     console.log("currently in:", $page.url.pathname)
    //     if (token != "no-token" && token != undefined){
    //         return
    //         // add requests for user's database
    //     }
    //     else {
    //         goto("/")
    //     }
    // })
</script>

<QuizPage quiz={quiz} />