import { writable } from "svelte/store";

export const QuizStore = writable({
    questions: [
        {
            question: "What is the answer?",
            options: ["1", "69", "42", "0"],
            correct_answers: ["69", "42"],
        },
        {
            question: "But for real, which is the right one?",
            options: ["this one!!!!", "NO, IT'S ME", "None", "The third one"],
            correct_answers: ["this one!!!!"],
        }
    ]
})

export const TextStore = writable(["test title", "test text"])
export const SummaryStore = writable({summary: ["test summary text"]})

export const AuthStore = writable("no-token")


