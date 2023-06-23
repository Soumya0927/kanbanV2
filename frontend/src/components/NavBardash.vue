<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <div class="container-fluid">
              <a class="navbar-brand">Kanban Board</a>
              <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
              </button>
              <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                <div class="navbar-nav">
                  <router-link class="nav-link active" aria-current="page" to="/summary">Summary</router-link>
                  <ul class="nav justify-content-end">
  <li class="nav-item">
    <a class="nav-link active" aria-current="page" v-on:click=logout>Logout</a>
  </li></ul>
                </div>
              </div>
            </div>
          </nav>
  </template>  
  <script>
  export default{
      name: "NavBardash",
      methods:{
        logout(){
            localStorage.removeItem('auth-token') 
            this.$router.push({ name: 'login' })

        }
      }
  };
  </script>