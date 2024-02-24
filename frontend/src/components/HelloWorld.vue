<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <p>
      Welcome To The Future of Teamwork.
      <!-- placeholder for a guide here -->
    </p>
    <h3>Developed By Students, For Students</h3>
    <p>
      This is a task management system to get s#it done.
    </p>
    <h3>Join Today To Achieve Your Goals</h3>
      <router-link :to="'RegisterUser'">Register</router-link>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
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
