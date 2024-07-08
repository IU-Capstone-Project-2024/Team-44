import { writable } from "svelte/store";

// figure this out ASAP!
export const QuizStore = writable({
    questions: [
        {
            question: "What is the answer?",
            options: ["1", "69", "42", "0"],
            correct_answers: ["69", "42"],
        },
        {
            question: "Kill count",
            options: ["0 :smileyface:", "39 buried 1 found", "none wtf", "NO"],
            correct_answers: ["39 buried 1 found"],
        }
    ]
})

export const TextStore = writable(["test title", "test text"])
export const SummaryStore = writable({summary: ["test summary tewxt"]})

export const AuthStore = writable({
})


