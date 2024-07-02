<script lang="ts">
    import LeftBar from "./LeftBar.svelte";
</script>

<div class="mainArea" style="display: flex;">
    <LeftBar />
    <div class="dragFiles">
        <p>Drag over your notes...</p>
    </div>
</div>


<style>
    .mainArea {
        height: 90vh;
        display: flex;
        flex-direction: row;
        flex: 100;
        background-color: white;
    }

    .dragFiles {
        display: flex;
        flex: 75;
        justify-content: center;
        align-items: center;
        background-color: white;
        border: 2 solid red;
    }
</style>
