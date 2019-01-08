<template>
    <div id="comm-main" class="module-box">
      <!--标题-->
      <div class="module-head clearfix">
        <h3>分享与交流</h3>
        <div class="module-head-oprt">
          <a class="el-button el-button--primary" type="button" href="">
            <i class="ico-submit"></i>
            我要发布
          </a>
        </div>
      </div>
      <!--讨论的分类标签-->
      <div class="discuss-tab-wrap">
        <a href="" class="discuss-tab">全部</a>
        <a href="" class="discuss-tab selected">其它1</a>
      </div>
    </div>
</template>

<script>
  export default {
    name: "CommMain"
  }
</script>

<style scoped>
  #comm-main {
    background-color: silver;
    height: 100%;
    flex:5;
  }
</style>
