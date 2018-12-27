<template>
  <div class="home">
    <!--走马灯-->
    <el-carousel height="400px" style="margin-top: 5px">
      <el-carousel-item v-for="item in 4" :key="item">
        <h3>{{ item }}</h3>
      </el-carousel-item>
    </el-carousel>
    <!--年终好课-->
    <div><img src="../assets/home/nzhk.png" alt="年终好课"></div>
    <ul id="nzhk">
      <li v-for="k in nzhk">
        <h2>{{k.name}}</h2>
        <h3>{{k.email}}</h3>
      </li>
    </ul>
    <!--各个板块-->
    <div id="ggbk-wrapper">
      <div class="bk" v-for="i in 4">
        <dl class="bk-name">
          <dt>
            <div><img src="../assets/home/arrow.png" alt=">"></div>
            <span>{{ggbk[0].name}}</span>
            <div class="bk-nav">板块导航</div>
          </dt>
          <hr>
        </dl>
        <div class="bk-content" v-for="c in ggbk[0].content">
          <a v-bind:href="c.url">{{c.title}}</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "Home",
    data() {
      return {
        nzhk: [],
        ggbk: [
          {
            name: "最新信息", content: [
              {title: "六级六级六级", url: "/"},
              {title: "六级六级六级", url: "/"},
              {title: "六级六级六级", url: "/"},
              {title: "六级六级六级", url: "/"},
            ]
          },
        ],
      }
    },
    created() {
      //TODO 获取年终好课

      this.$http.get("http://jsonplaceholder.typicode.com/users")
        .then((data) => {
            this.nzhk = data.body;
          }
        );

      //TODO 获取各个板块首发信息
    }
  }
</script>

<style scoped>
  .el-carousel__item h3 {
    color: #475669;
    font-size: 14px;
    opacity: 0.75;
    line-height: 150px;
    margin: 0;
  }

  .el-carousel__item:nth-child(2n) {
    background-color: #99a9bf;
  }

  .el-carousel__item:nth-child(2n+1) {
    background-color: #d3dce6;
  }

  /*-----------------------------------------------------------*/

  #nzhk {
    /*弹性布局*/
    display: flex;
    /*弹性元素在必要时换行*/
    flex-wrap: wrap;
    /*清除列表标记项的类型*/
    list-style-type: none;
    padding: 0;
  }

  #nzhk li {
    /*当父元素的宽度大于所有子元素的宽度的和时,索取剩余空间*/
    flex-grow: 1;
    /*弹性元素的原始宽度*/
    flex-basis: 200px;
    text-align: center;
    padding: 30px;
    border: 1px solid #222;
    margin: 10px;
  }

  /*-----------------------------------------------------------*/

  #ggbk-wrapper {
    width: 90%;
    margin: 0 auto;
  }

  .bk {
    width: 100%;
    background-color: lavender;
    margin: 10px 0;
  }

  .bk-name {
    text-align: left;
  }

  dt{
    display: flex;
    align-items: center;
  }

  dt span{
    flex: 1;
    font-size: 20px;
  }

  dt .bk-nav{
    background-color: white;
  }

  dd{
    background-color: white;
  }

</style>
