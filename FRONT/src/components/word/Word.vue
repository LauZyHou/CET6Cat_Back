<template>
  <div id="word">
    <h2>背单词页面</h2>
      <app-card></app-card>
  </div>
</template>

<script>
  import Card from './Card'

  export default {
    name: "Word",
    components: {
      "app-card": Card
    }
  }
</script>

<style>
  #word{
    width: 100%;
    background-color: lavender;
    height: 100%;
  }
</style>
