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
      <a href="" class="discuss-tab selected">全部</a>
      <a href="" class="discuss-tab">其它1</a>
    </div>
    <!--菜单盒子-->
    <div class="menu-txt-box">
      <ul class="menu-txt clearfix">
        <li class="selected">
          <a href="">最新回复</a>
        </li>
        <li class="menu-pipe">|</li>
        <li>
          <a href="">最新发表</a>
        </li>
      </ul>
    </div>
    <!--主要内容区域-->
    <div class="module-body">
      FIXME 这里是主要内容
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
    /*background-color: antiquewhite;*/
    height: 100%;
    flex: 5;
  }

  /*-----------------------------------------------------------*/

  .module-head h3 {
    float: left;
  }

  .module-head .module-head-oprt {
    float: right;
  }

  /*-----------------------------------------------------------*/

  .discuss-tab-wrap {
    background: #f5f5f5;
    padding: 15px 15px 10px;
    margin: 10px 0 0;
  }

  .discuss-tab {
    padding: 0 5px;
    height: 28px;
    line-height: 28px;
    display: inline-block;
    white-space: nowrap;
    font-size: 14px;
    margin: 0 10px 5px 0;
  }

  .discuss-tab.selected {
    background: #25bb9b;
    color: #fff;
    text-align: center;
  }

  /*-----------------------------------------------------------*/

  .menu-txt {
    letter-spacing: -4px;
    white-space: nowrap;
  }

  .menu-txt li {
    letter-spacing: 0;
    display: inline-block;
    margin-right: 1px;
    position: relative;
  }

  .menu-pipe {
    padding: 0 8px;
    color: #959595;
    vertical-align: 1px;
  }
</style>
