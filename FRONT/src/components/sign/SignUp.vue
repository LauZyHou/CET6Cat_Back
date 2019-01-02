<template>
  <div id="sign-up">
    <h3>现在注册CET6Cat</h3>
    <el-form :model="user" :rules="rules" ref="user" label-width="100px" class="">
      <el-form-item label="邮箱" prop="email">
        <el-input v-model="user.email"></el-input>
      </el-form-item>
      <el-form-item label="昵称" prop="name">
        <el-input v-model="user.name"></el-input>
      </el-form-item>
      <el-form-item label="入学年份" prop="year_in">
        <el-select v-model="user.year_in" placeholder="请选择入学年份">
          <el-option label="2015" value="2015"></el-option>
          <el-option label="2016" value="2016"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="薄弱项" prop="weak_items">
        <el-checkbox-group v-model="user.weak_items">
          <el-checkbox label="写作" name="type"></el-checkbox>
          <el-checkbox label="听力" name="type"></el-checkbox>
          <el-checkbox label="阅读" name="type"></el-checkbox>
          <el-checkbox label="翻译" name="type"></el-checkbox>
        </el-checkbox-group>
      </el-form-item>
      <el-form-item label="性别" prop="sex">
        <el-radio-group v-model="user.sex">
          <el-radio label="男"></el-radio>
          <el-radio label="女"></el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="邀请码" prop="yq_code">
        <el-input type="textarea" v-model="user.yq_code"></el-input>
      </el-form-item>
      <el-form-item label="订阅CET6Cat" prop="subs">
        <el-switch v-model="user.subs"></el-switch>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm('user')">立即注册</el-button>
        <el-button @click="resetForm('user')">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
  export default {
    name: "SignUp",
    data() {
      return {
        user: {
          email: '',
          name: '',
          year_in: '',
          weak_items: [],
          sex: '',
          yq_code: '',
          subs: true,
        },
        rules: {
          email: [
            {required: true, message: '请输入邮箱', trigger: 'blur'},
            {min: 7, max: 30, message: '请输入正确的邮箱', trigger: 'blur'}
          ],
          name: [
            {required: true, message: '请输入昵称', trigger: 'blur'},
            {min: 3, max: 7, message: '长度在 3 到 7 个字符', trigger: 'blur'}
          ],
          year_in: [
            {required: true, message: '请选择入学年份', trigger: 'change'}
          ],
          weak_items: [
            {type: 'array', required: true, message: '制定更好的学习计划', trigger: 'change'}
          ],
          sex: [
            {required: true, message: '请选择性别', trigger: 'change'}
          ]
        }
      };
    },
    methods: {
      submitForm(formName) {
        //FIXME
        this.$refs[formName].validate((valid) => {
          if (valid) {
            alert('submit!');
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      resetForm(formName) {
        this.$refs[formName].resetFields();
      }
    }
  }
</script>

<style scoped>
  #sign-up {
    width: 70%;
    margin: 0 auto;
    padding: 22px 0;
    background-color: lavender;
  }

  .el-form > .el-form-item {
    width: 70%;
    margin: 0 auto 22px;
    /*display: flex;*/
    /*flex-wrap: nowrap;*/
  }

  .el-select {
    width: 100%;
  }
</style>
