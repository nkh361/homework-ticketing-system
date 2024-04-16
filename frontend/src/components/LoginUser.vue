<template>
    <div class="LoginUser">
      <h2>Login Here!</h2>
      <form name="loginForm">
        <input type="text" v-model="loginFormData.username" placeholder="New Username">
        <input type="password" v-model="loginFormData.password" placeholder="New Password">
        <button @click.prevent="loginUser">Submit</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'LoginUser',
    data() {
      return {
        loginFormData: {
          username: '',
          password: ''
        }
      };
    },
    methods: {
      loginUser() {
        const path = 'http://127.0.0.1:5000/login'
        axios.post(path, {
          "username": this.loginFormData.username,
          "password": this.loginFormData.password
        })
        .then((res) => {
          console.log(res.data)
          // this.$router.push({path: '/dashboard'})
        })
        .catch((err) => {
          console.error(err)
        })
      }
    },
    created() {
      this.loginUser();
    }
  };
  </script>
  
  
  <style scoped>
  h2 {
    margin: 40px 0 0;
  }
  
  input[type=text]:focus {
      background-color: #84ceac;
  }
  
  
  input[type=password]:focus {
    background-color: #84ceac;
  }
  </style>