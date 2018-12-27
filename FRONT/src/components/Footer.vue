<template>
  <footer><p>{{copyright}}</p></footer>
</template>

<script>
  export default {
    name: "Footer",
    data() {
      return {
        copyright: "Copyright©2018-2019 Zhihao Liu at SHU"
      }
    }
  }
</script>

<style scoped>
  footer {
    background: rgb(84, 92, 100);
    padding: 6px;
  }

  p {
    color: white;
    text-align: center;
  }
</style>
