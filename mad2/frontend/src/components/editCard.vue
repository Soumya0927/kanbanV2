<template>
    <div class="form-container">
    <form  method="POST" id="update-listcard-form" >
        <label for="list" class = "col-sm-2 col-form-label">Want to shift to another list?: </label>
        <select v-model="editcardData.list_belong" placeholder="want to change list?">
				<option v-for="list in get_list" v-bind:key="list.lid" v-bind:value="list.lid">{{ list.list_name }}</option>
			</select>
        <div class="mb-3">
            <label  class="col-sm-2 col-form-label">Card Title: </label>
            <input type="text" class="form-control" v-model = editcardData.Title required >
        </div>
        <div class="mb-3">
            <label  class="col-sm-2 col-form-label">Content: </label>
            <input type="text" class="form-control" v-model = editcardData.Content rows="3"/>
        </div>
        <label for="date" class="col-sm-2 col-form-label">Deadline Date: </label>
        <input type="date" class="form-control" id="date" v-model = editcardData.Deadline name = "Deadline" />
              
    
        <div class="form-check form-switch">
          <input class="form-check-input" type="checkbox" v-model="editcardData.Flag" @click="toggleCheckbox">          <!--<input class="form-check-input" type="hidden" id="flexSwitchCheckChecked" v-model="addcardData.Flag" value = "off">--> 
          <label class="form-check-label" for="flexSwitchCheckChecked">Mark as complete</label>
        </div>
    
    
        <div class="col-5">
          <router-link to="/about" type="button" class="btn btn-primary">Cancel</router-link>
    &nbsp;
            <button type="submit" @click.prevent="editCard" class="btn btn-primary">Save</button>
        </div>
    </form>
    </div>
    
    <div>
        <p>Card Created : {{editcardData.card_created}}</p>
        <p> Last Updated : {{editcardData.last_change}} </p> 
    </div></template>

<script>
export default {
      name: 'editCard',
    data() {
      return {
        editcardData:{
        Title: "",
        Content:"",
        Deadline:"",
        Flag:false,
        card_created:"",
        last_change:"",
        list_belong:""
      },
      get_list:[]
      //name:this.$route.params.name
    }},
    async mounted() {
    await fetch ("http://localhost:5000/api/allList",
    {mode:'cors',
    method:"GET",
        authRequired: true,
        headers:{
          'Authentication-Token':localStorage.getItem('auth-token')
        }
    }).then((response) => response.json())
      .then((data) => {
          console.log(data)
        this.get_list=data['result']
      })
          .catch((err) => {
          this.error = err.message
          console.log(err)
        });
    if (this.$route.params.id){
    await fetch('http://localhost:5000/api/card/'+this.$route.params.id,
    {mode:'cors',
    method:"GET",
        authRequired: true,
        headers:{
          'Authentication-Token':localStorage.getItem('auth-token')
        }
    }).then((response) => response.json())
      .then((data) => {
          console.log(data["list_id"])
        this.editcardData.Title= data['card_title'];
        this.editcardData.Content=data['content'];
        this.editcardData.Deadline=data['deadline'];
        this.editcardData.Flag=data["flag"];
        this.editcardData.card_created=data["card_created"];
        this.editcardData.last_change=data["last_change"];
        this.editcardData.list_belong = data["list_id"]
         
        })
        .catch((err) => {
          this.error = err.message
          console.log(err)
        })
    }},
    methods: {
    async editCard() {
    console.log("msg",this.editcardData)
    await fetch('http://localhost:5000/api/editcard/'+this.$route.params.id,
    {mode: 'cors',
    method: 'PUT',
    headers: { 'Content-Type': 'application/json',
    'Authentication-Token':localStorage.getItem('auth-token') },
    body: JSON.stringify(this.editcardData)
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