<template>    
  <div class="form-container">
<form style="border:1px solid #ccc" method = "post"> 
  <h1>Sign Up</h1>
    <p>Please fill in this form to create an account.</p>
    <div class="row justify-content-center">
    <label class="col-sm-2 col-form-label">Name</label>
    <input type="text" class="form-control"  v-model = "signupData.username" required/> 
</div>    
<div class="row justify-content-center">
    <label class="col-sm-2 col-form-label">Email</label>
    <input type="email" class="form-control"  v-model = "signupData.email" required/>
</div>
<div class="row justify-content-center">
    <label class="col-sm-2 col-form-label">Password</label>
    <input type="password" class="form-control" v-model = "signupData.password" required/>
</div>
<button @click.prevent="SignUp" type="submit" class="btn btn-primary">Sign in</button>
</form>
  </div>
</template>
<script>
//import axios from 'axios'
  export default {
      name: 'SignupUser',
    data() {
      return {
        signupData:{
        username: "",
        email: "",
        password: "",
      }
    };
    },
    methods: {
     
      async SignUp() {
    console.log("msg",this.signupData)
    await fetch('http://localhost:5000/api/users', {
    mode: 'cors',
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(this.signupData),
    }).then(function (data) {
    console.log('Request succeeded with JSON response', data);
    routes.push("/login")
    })
    .catch(function (error) {
    console.log('Request failed', error);
    });/*
      axios.post('http://localhost:5000/api/users', this.signUpData,
      {
        headers:{
          'Content-Type':'application/x-www-form-urlencoded'f
        }
      })
                 .then((res) => {
                  alert('User Created',res)
          this.$router.push("/login")
        })
        .catch((err) => {
          alert(err)
        })
      const res = fetch(
         "http://localhost:5000/api/users",
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.signUpData),
        },
      )
        
      res
        .then(() => {
          alert('User Created',res)
          this.$router.push("/login")
        })
        .catch((err) => {
          alert(err)
        })*/
    }
  }
    };
import routes from '../router/index.js'
</script>
<style>
   .form-container {
  display:table;
  max-width:900px;
  width:90%;
  margin:0 auto;
  box-shadow:1px 1px 5px rgba(0,0,0,0.1);
}

form {
  display:table-cell;
  width:400px;
  background-color:#ffffff;
  padding:40px 60px;
  color:#505e6c;
}



 form h2 {
  font-size:24px;
  line-height:1.5;
  margin-bottom:30px;
}

 form .form-control {
  background:#f7f9fc;
  border:none;
  border-bottom:1px solid #dfe7f1;
  border-radius:0;
  box-shadow:none;
  outline:none;
  color:inherit;
  text-indent:6px;
  height:40px;
}

 form .form-check {
  font-size:13px;
  line-height:20px;
}

 form .btn-primary {
  background:#f4476b;
  border:none;
  border-radius:4px;
  padding:11px;
  box-shadow:none;
  margin-top:35px;
  text-shadow:none;
  outline:none !important;
}

 form .btn-primary:hover, .register-photo form .btn-primary:active {
  background:#eb3b60;
}

form .btn-primary:active {
  transform:translateY(1px);
}

form .already {
  display:block;
  text-align:center;
  font-size:12px;
  color:#6f7a85;
  opacity:0.9;
  text-decoration:none;
}


</style>