<script lang="ts">
    import Paper, {Subtitle, Title} from "@smui/paper";
    import Navbar from "../../static/Navbar.svelte";
</script>


<div class="about-container">
    <div class="text-container">
        <div class="title">
            <div class="mdc-typography--headline3">About the program</div>
        </div>
        <div class="title">
            <div class="mdc-typography--headline5">
                Our project is a unique web platform designed to help Innopolis University students organize their study materials, manage their time effectively, and enhance their learning efficiency. Our platform offers powerful features like automatic quiz generation from notes and note summarization, helping you excel in your academic endeavors.
            </div>
        </div>
    </div>
    <div class="two-feats">
        <div class="text-container">
            <div class="title">
                <div class="mdc-typography--headline3">Note Summarization</div>
            </div>
            <div class="title">
                <div class="mdc-typography--headline5">
                    By uploading your notes and selecting the summarization option, you will receive a compressed version of your notes highlighting the key points and essential information. This is useful for quick review and exam preparation.
                </div>
            </div>
        </div>
        <div class="text-container">
            <div class="title">
                <div class="mdc-typography--headline3">Quiz Generation</div>
            </div>
            <div class="title">
                <div class="mdc-typography--headline5">
                    You will receive a set of questions with multiple-choice answers that help you test your knowledge and reinforce your understanding of the material. Quizzes are an excellent tool for self-assessment and deepening your grasp of the subject.
                </div>
            </div>
        </div>
    </div>

</div>


<style>
    .about-container {
        display: flex;
        flex-direction: column;
        justify-content:space-evenly;
        height: min(max(80%, 300px), 600px);
        width: min(max(80%, 500px), 1400px);
    }

    .text-container {
        padding: 10px;
        background-color: #333;
        display:flex;
        justify-content:center;
        flex-direction:column;
        border: 1px solid #ff3e00;
        border-radius: 10px;

    }
    .title {
        display: flex;
        justify-content: center;
        padding: 10px 5%;
    }
    .two-feats {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
    }
</style>