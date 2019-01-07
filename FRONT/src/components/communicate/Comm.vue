<template>
  <div id="comm">
    <h3>这里是交流论坛</h3>
    <div class="container">
      <comm-main></comm-main>
      <comm-aside></comm-aside>
    </div>
  </div>
</template>

<script>
  import CommMain from './CommMain'
  import CommAside from './CommAside'

  export default {
    name: "Comm",
    components: {
      "comm-main": CommMain,
      "comm-aside": CommAside
    }
  }
</script>

<style scoped>

  .container {
    display: flex;
    height: 800px;
    margin-bottom: 10px;
  }
</style>

<style>
  #comm-main{
    margin-right: 10px;
  }
</style>
