<script lang="ts">
    import { onMount } from "svelte";
    import { AuthStore } from "../../../../data-store";
    import { goto } from "$app/navigation";
    import { page } from "$app/stores";
    import { QuizStore } from "../../../../data-store";
    import QuizPage from "../../../../static/QuizPage.svelte";

    let quiz = $QuizStore
    let sample = {
            question: "Sample Question",
            options: ["ans1", "ans2", "ans3", "ans4"],
            correct_answers: ["ans1"],
        }
    onMount(() => {
        let token = $AuthStore
        console.log("token:", token)
        console.log("currently in:", $page.url.pathname)
        if (quiz.questions.length == 1 && quiz.questions[0] == sample){
            goto("/send")
        }
        else if (token == "no-token" || token == undefined){
            goto("/")
        }
    })
</script>

<QuizPage quiz={quiz} />