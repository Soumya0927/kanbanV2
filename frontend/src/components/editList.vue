<template>
<h1>Update List</h1>
<div class="form-container">
<form method="POST" id="update-list-form">
    <div>
        <label class="col-sm-2 col-form-label">List Name:</label>
        <input type="text" v-model = editlistData.lname required /><br><br><br><br>
    </div>
    <div>
        <label class = "col-sm-2 col-form-label">Description:</label>
        <input type="text" v-model = editlistData.desc required /><br><br><br><br>
    </div>
    <div class="col-5">
        <router-link to="/about" type="button" class="btn btn-primary">Cancel</router-link>
    &nbsp;
        <button @click.prevent="editList" type="submit" class="btn btn-primary">Save</button>
    </div>
</form></div></template>
<script>
export default {
      name: 'editList',
    data() {
      return {
        editlistData:{
        lname: "",
        desc: ""
      },
      //name:this.$route.params.name
    }},
    async mounted() {
    if (this.$route.params.name) {
    await fetch('http://localhost:5000/api/tasks/'+this.$route.params.name,
    {   mode:'cors',
    method:"GET",
        authRequired: true,
        headers:{
          'Authentication-Token':localStorage.getItem('auth-token')
        }
    }).then((response) => response.json())
      .then((data) => {
          console.log(data)
          this.editlistData.lname = data['list_name'];
          this.editlistData.desc = data['description']
        })
        .catch((err) => {
          this.error = err.message
          console.log(err)
        })
    }},
    methods: {
    async editList() {
    console.log("msg",this.editlistData)
    await fetch('http://localhost:5000/api/editlist/'+this.$route.params.name,
    {mode: 'cors',
    method: 'PUT',
    headers: { 'Content-Type': 'application/json',
    'Authentication-Token':localStorage.getItem('auth-token') },
    body: JSON.stringify(this.editlistData)
    }).then(function (data) {
    console.log('Request succeeded with JSON response', data);
    routes.push("/about")
    })
    .catch(function (error) {
    console.log('Request failed', error);
    });
}}}
import routes from '../router/index.js'
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