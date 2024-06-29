import { writable } from "svelte/store";


export const DataStore = writable([
    {type: "note", id: 0, content: "test", date: "01-01-1970"}
])

export const AuthStore = writable({
})

