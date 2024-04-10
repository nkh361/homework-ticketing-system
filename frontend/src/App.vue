<template>
  <img alt="Vue logo" src="./assets/logo.png">
  <LandingMessage :msg="'One for All Coworking'"/>
  <RegisterUser></RegisterUser>
</template>

<script>
import LandingMessage from './components/IntroductionPage.vue';
import RegisterUser from './components/RegisterUser.vue';

export default {
  name: 'App',
  components: {
    LandingMessage,
    RegisterUser
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
