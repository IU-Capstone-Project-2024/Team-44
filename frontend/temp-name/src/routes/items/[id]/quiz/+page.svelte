<script lang="ts">
    import { QuizStore } from "../../../../data-store";
    import QuizPage from "../../../../static/QuizPage.svelte";

    let quiz = $QuizStore
</script>

<QuizPage quiz={quiz} />