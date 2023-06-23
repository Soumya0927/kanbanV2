<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <router-link to="/login"><button @click="login"> Login</button></router-link>
    <router-link to="/signup"><button @click="signup">Signup</button></router-link>

    <router-view />
  </div>
</template>

<script>
export default {
  name: "HelloWorld",
  data() {
    return {
      msg: "",
    };
  },

  // props: {
  //   msg: String,
  // },
  mounted() {
    fetch("http://localhost:5000/api/")
      .then((response) => response.json())
      .then((data) => {
        this.msg = data["msg"];
      });
  },
  methods: {
    login() {
      this.$router.push({ name: 'login' })
    },
    signup() {
      this.$router.push({ name: 'signup' })
    }
}};
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
