<script lang="ts">
import QuizPage from "../../static/QuizPage.svelte";
let quiz : any = {
    quests: [
        {
            question: "What is the answer?",
            options: ["1", "69", "42", "0"],
            answer: ["69", "42"],
            number: 1
        },
        {
            question: "Kill count",
            options: ["0 :smileyface:", "39 buried 1 found", "none wtf", "NO"],
            answer: ["39 buried 1 found"],
            number: 2
        }
    ]
}
export let questNum = 0

</script>

<QuizPage 
question={quiz.quests[questNum].question} 
options={quiz.quests[questNum].options} 
answer={quiz.quests[questNum].answer} 
/>