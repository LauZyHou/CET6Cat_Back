<template>
  <div class="user-table">
    <el-row display="margin-top:10px">
      <el-input v-model="input" placeholder="请输入姓名" style="display:inline-table; width: 30%; float:left"></el-input>
      <el-button type="primary" @click="addUser()" style="float:left; margin: 2px;">新增</el-button>
    </el-row>
    <el-row>
      <el-table :data="userList" style="width: 100%" border>
        <el-table-column prop="id" label="编号" min-width="100">
          <template scope="scope"> {{ scope.row.pk }}</template>
        </el-table-column>
        <el-table-column prop="book_name" label="user_name" min-width="100">
          <template scope="scope"> {{ scope.row.fields.user_name }}</template>
        </el-table-column>
      </el-table>
    </el-row>
  </div>
</template>

<script>
  export default {
    name: "UserTable",
    data() {
      return {
        input: '',
        userList: [],
      }
    },
    mounted: function () {
      this.getUsers()
    },
    methods: {
      addUser() {
        this.$http.get('/api/tst/add_user?user_name=' + this.input)
          .then((response) => {
            let res = JSON.parse(response.bodyText);
            if (res.error_num === 0) {
              this.getUsers();
            } else {
              this.$message.error('新增User失败，请重试');
              console.log(res['msg']);
            }
          })
      },
      getUsers() {
        this.$http.get('/api/tst/get_users')
          .then((response) => {
            let res = JSON.parse(response.bodyText);
            console.log(res);
            if (res.error_num === 0) {
              this.userList = res['list'];
            } else {
              this.$message.error('查询User失败');
              console.log(res['msg']);
            }
          })
      }
    }
  }
</script>

<style scoped>
  h1, h2 {
    font-weight: normal;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    display: inline-block;
    margin: 0 10px;
  }

  a {
    color: #42b983;
  }
</style>
