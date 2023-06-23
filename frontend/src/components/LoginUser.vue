<template><NavBar />
    <h3> Welcome to Kanban App!</h3>
    <div class="form-container">
    <form method="post">
        <div class="mb-3 mt-3">
            <label for="user_name" class="form-label">Email : </label>
            <input type="email" class="form-control" id="email" placeholder="Enter email" v-model = "LoginData.email" required />
        </div>
        <div class="mb-3 mt-3">
            <label for="pwd" class="form-label">Password :  </label>
            <input type="password" class="form-control" id="pwd" placeholder="Enter password" v-model = "LoginData.password" required />
        </div>
        <div class="mb-3 mt-3">
            <label class="form-check-label">
            <input class="form-check-input" type="checkbox" name="remember"> Remember me</label>
     </div>
        <button @click.prevent="Login" type="submit" class="btn btn-primary">Submit</button>
      </form>
    </div>
    </template>
    <script>
    import NavBar from '@/components/NavBar.vue'
    
      export default {
          name: 'LoginUser',
        data() {
          return {
            LoginData:{
        email: "",
        password: "",
      }};
        },
        components:{
          NavBar
        },
        methods: {
         async Login(){
        const res = await fetch('http://localhost:5000/login?include_auth_token', {
        method: 'post',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.LoginData),
      })

      if (res.ok) {
        const data = await res.json()
        localStorage.setItem(
          'auth-token',
          data.response.user.authentication_token
        )
         alert('login')
          this.$router.push('about')
        }
        else{
          console.log("Something went wrong")
        }
      }
  }
      };
    </script>
    <style>   .form-container {
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