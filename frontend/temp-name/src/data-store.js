import { writable } from "svelte/store";

// figure this out ASAP!
export const DataStore = writable({
    text: "lorem ipsum dolor res",
    summary: "lorem dolor",
    quiz: {
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
})

export const AuthStore = writable({
})


