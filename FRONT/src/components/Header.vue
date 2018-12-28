<template>
  <header>
    <div class="top-bar">
      <span>你好,欢迎来到CET6Cat</span>
      <span class="space">|</span>
      <router-link rel="nofollow" to="#">注册</router-link>
      <span class="space">|</span>
      <router-link rel="nofollow" to="#">登录</router-link>
    </div>
    <!------------------------------------------------------------->
    <div class="top-show">
      <div class="logo">
        <!--<h2>CET6Cat六级辅导</h2>-->
        <img src="../assets/vue.png" alt="Vue.js"/>
      </div>
      <div class="top-search">
        <el-input placeholder="请输入内容" v-model="input5" class="input-with-select">
          <el-select v-model="select" slot="prepend" placeholder="请选择" value="2">
            <el-option label="课程" value="1"></el-option>
            <el-option label="新闻" value="2"></el-option>
            <el-option label="用户" value="3"></el-option>
          </el-select>
          <el-button slot="append" icon="el-icon-search"></el-button>
        </el-input>
      </div>
    </div>
    <!------------------------------------------------------------->
    <div class="top-nav">
      <el-menu
        :default-active="activeIndex2"
        class="el-menu-demo"
        mode="horizontal"
        @select="handleSelect"
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b"
        router="true">
        <el-menu-item index="/">主页</el-menu-item>
        <el-submenu index="2">
          <template slot="title">最新信息</template>
          <el-menu-item index="2-1">选项1</el-menu-item>
          <el-menu-item index="2-2">选项2</el-menu-item>
          <el-menu-item index="2-3">选项3</el-menu-item>
          <el-submenu index="2-4">
            <template slot="title">选项4</template>
            <el-menu-item index="2-4-1">选项1</el-menu-item>
            <el-menu-item index="2-4-2">选项2</el-menu-item>
            <el-menu-item index="2-4-3">选项3</el-menu-item>
          </el-submenu>
        </el-submenu>
        <el-menu-item index="3" disabled>在线模拟</el-menu-item>
        <el-menu-item index="4">慕课视频</el-menu-item>
        <el-menu-item index="5">交流论坛</el-menu-item>
        <el-menu-item index="/word">背单词打卡</el-menu-item>
        <el-menu-item index="7">阅读分析</el-menu-item>
        <el-menu-item index="8">高分作文交流汇</el-menu-item>
      </el-menu>
    </div>
  </header>
</template>

<script>
  export default {
    name: "Header"
  }
</script>

<style scoped>
  .top-bar {
    width: 100%;
    margin: 0 auto;
    line-height: 36px;
    height: 36px;
    background: #fff;
    z-index: 1000;
    /*随动*/
    position: fixed;
    top: 0;
    left: 0;
    /*透明*/
    filter: alpha(Opacity=80);
    -moz-opacity: 0.5;
    opacity: 0.5;
  }

  .top-bar:hover {
    /*取消透明*/
    filter: alpha(Opacity=100);
    -moz-opacity: 100;
    opacity: 100;
  }

  /*竖线*/
  .space {
    padding: 0 8px;
    color: #959595;
  }

  /*-----------------------------------------------------------*/

  .top-show {
    z-index: 4;
    margin-top: 17px;
    width: 96%;
    background: #fff;
    height: 80px;
    display: flex;
    /*垂直居中*/
    align-items: center;
  }

  header, .top-show {
    position: relative;
  }

  .top-search {
    flex: 7;
  }

  .el-select .el-input {
    width: 130px;
  }

  .logo {
    flex: 1;
    height: 40px;
    width: 40px;
  }

  .logo {
    /*background: url("../assets/vue.png") no-repeat 5px 5px;*/
  }

  /*图片总是尽量占满*/
  img {
    width: auto;
    height: auto;
    max-width: 100%;
    max-height: 100%;
  }

  /*-----------------------------------------------------------*/


</style>
