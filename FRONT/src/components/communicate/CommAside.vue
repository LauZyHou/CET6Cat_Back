<template>
  <div id="comm-aside" class="module-box">
    <!--热门话题-->
    <div class="module-box">
      <div class="module-head clearfix">
        <h3>热门话题</h3>
        <a href="">查看全部</a>
      </div>
      <div class="module-body">
        <div class="tags-box">
          <a href="">标签名</a>
          <a href="">标签名</a>
          <a href="">标签名</a>
        </div>
      </div>
    </div>
    <!--近期热帖-->
    <div class="module-box">
      <div class="module-head clearfix">
        <h3>近期热帖</h3>
      </div>
      <div class="module-body">
        <ul class="list-module">
          <li v-for="i in 7">
            <div class="list-title">
              <a target="_blank" class="list-name" href="">找个博士毕业年薪50万+ 要求高不</a>
            </div>
            <div class="list-legend">
              <span class="comm-num">
                回复<a target="_blank" href="">(65)</a>
              </span>
              发表于 今天 12:57:08
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "CommAside"
  }
</script>

<style scoped>
  #comm-aside {
    background-color: silver;
    height: 100%;
    flex: 1;
  }

</style>
