import { writable } from "svelte/store";

export const QuizStore = writable({
    questions: [
        {
            question: "Sample Question",
            options: ["ans1", "ans2", "ans3", "ans4"],
            correct_answers: ["ans1"],
        }

    ]
})

export const TextStore = writable(["test title", "test text"])
export const SummaryStore = writable({summary: "test summary text"})

export const AuthStore = writable("no-token")


