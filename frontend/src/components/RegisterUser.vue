<template>
  <div class="RegisterUser">
    <h2>Register Here!</h2>
    <form name="registerForm">
      <input type="text" v-model="registerFormData.username" placeholder="New Username">
      <input type="password" v-model="registerFormData.password" placeholder="New Password">
      <input type="text" v-model="registerFormData.email" placeholder="Enter your email">
      <button @click.prevent="registerUser">Submit</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'RegisterUser',
  data() {
    return {
      registerFormData: {
        username: '',
        password: ''
      }
    };
  },
  methods: {
    // registerUser() {
    //   const path = 'http://127.0.0.1:5000/register'
    //   axios.get(path, this.registerFormData)
    //   .then((res) => {
    //     console.log(res.data)
    //   })
    //   .catch((err) => {
    //     console.error(err)
    //   })
    // }
    registerUser() {
      const path = 'http://127.0.0.1:5000/register'
      axios.post(path, {
        "username": this.registerFormData.username,
        "password": this.registerFormData.password,
        "email": this.registerFormData.email
      })
      .then((res) => {
        console.log(res.data)
        this.$router.push({path: '/dashboard'})
      })
      .catch((err) => {
        console.error(err)
      })
    }
  },
  created() {
    this.registerUser();
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