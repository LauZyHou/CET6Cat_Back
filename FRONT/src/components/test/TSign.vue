<template>
  <div id="t-sign">
    <h3>这里是测试登录</h3>
    <form action="http://localhost:8000/tst/validate" method="post">
      用户名:<br>
      <input type="text" name="user_name" value="Flora">
      <br>
      密码:<br>
      <input type="text" name="password" value="111111">
      <br><br>
      <input type="submit" value="提交">
    </form>

    <hr>

    <h3>这里是测试注册</h3>
    <form action="http://localhost:8000/tst/validate" method="post">
      用户名:<br>
      <input type="text" name="user_name" value="Flora">
      <br>
      密码:<br>
      <input type="text" name="password" value="111111">
      <br>
      验证码:<br>
      <input type="text" name="password" value="1234">
      <br><br>
      <input type="submit" value="提交">
    </form>

  </div>
</template>

<script>
  export default {
    name: "TSign",
    methods: {
      // 检查数据
      check_username: function () {
        if (!this.username) {
          this.error_username = true;
        } else {
          this.error_username = false;
        }
      },
      check_pwd: function () {
        if (!this.password) {
          this.error_pwd_message = '请填写密码';
          this.error_pwd = true;
        } else {
          this.error_pwd = false;
        }
      },
      // 表单提交
      on_submit: function () {
        this.check_username();
        this.check_pwd();

        if (this.error_username == false && this.error_pwd == false) {
          axios.post(this.host + '/tk/', {
            username: this.username,
            password: this.password
          }, {
            responseType: 'json',
            withCredentials: true
          }).then(response => {
            console.log(response.data.token);
              // 使用浏览器本地存储保存token
              if (this.remember) {
                // 记住登录
                sessionStorage.clear();
                localStorage.token = response.data.token;
                localStorage.user_id = response.data.user_id;
                localStorage.username = response.data.username;
              } else {
                // 未记住登录
                localStorage.clear();
                sessionStorage.token = response.data.token;
                sessionStorage.user_id = response.data.user_id;
                sessionStorage.username = response.data.username;
              }

              // 跳转页面
              var return_url = this.get_query_string('next');
              if (!return_url) {
                return_url = '/index.html';
              }
              location.href = return_url;
            })
            .catch(error => {
              if (error.response.status === 400) {
                this.error_pwd_message = '用户名或密码错误';
              } else {
                this.error_pwd_message = '服务器错误';
              }
              this.error_pwd = true;
            })
        }
      },
      // qq登录
      qq_login: function(){

      }
    }, data() {
      return {
        remember: true,
        error_pwd: false,
        error_username: false,
        username: "",
        password: "",
        error_pwd_message: "",
        host:"http://localhost:8000"
      }
    }
  }
</script>

<style scoped>

</style>
