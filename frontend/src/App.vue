<template>
  <img alt="Vue logo" src="./assets/logo.png">
  <LandingMessage :msg="'One for All Coworking'"/>
  <!-- <RegisterUser></RegisterUser> -->
  <LoginUser>Login</LoginUser>
  <!-- <RegisterUser></RegisterUser>
  <UserDashboard></UserDashboard>
  <a href="/dashboard">Dashboard</a>
  <LoginUser></LoginUser> -->
</template>

<script>
import LandingMessage from './components/IntroductionPage.vue';
// import RegisterUser from './components/RegisterUser.vue';
// import UserDashboard from './components/UserDashboard.vue';
import LoginUser from './components/LoginUser.vue';

export default {
  name: 'App',
  components: {
    LandingMessage,
    // RegisterUser,
    // UserDashboard,
    LoginUser
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
