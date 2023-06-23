<template>
  <div class="home">
    <NavBar />
<h3>Create and View your Tasks</h3>
      <p></p>

    <img alt="" src="../assets/home.jpg" >
    <p><router-link class="btn btn-lg btn-primary" to="/signup" role="button">Sign up today</router-link>
   </p> <!--HelloWorld /-->
   <!-- <router-view></router-view>-->
  </div>
</template>
<script>
// @ is an alias to /src
//import HelloWorld from '@/components/HelloWorld.vue'
import NavBar from '@/components/NavBar.vue'

export default {
  name: 'HomeView',
  components: {
    //HelloWorld,
    NavBar
  }
}
</script>
<style>

</style>
