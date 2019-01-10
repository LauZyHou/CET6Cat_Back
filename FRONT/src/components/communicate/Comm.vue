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
  #comm-main {
    margin-right: 10px;
  }

  .module-box {
    background-color: white;
    border: 1px solid #e0e0e0;
    border-radius: 3px;
  }

  .module-head{
    padding: 15px 15px 0;
  }

  body {
    /*FIXME 调整font字体*/
  }

  /*小红点*/
  .module-head h3::before{
    background: #ff6547;
    content: "";
    display: inline-block;
    width: 7px;
    height: 7px;
    margin-right: 5px;
    margin-bottom: 2px;
    vertical-align: middle;
  }
</style>
