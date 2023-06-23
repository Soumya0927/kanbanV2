<template>
<div class="form-container">
    <form method = 'post'>
        <!--<label for="list" class="col-sm-2 col-form-label">Select list: </label>
        <select v-model="addcardData.list" >
            <div>
            <option v-for="(key) in get_list" v-bind:key= "`${key[lid]}`" selected>{{key[list_name]}}</option>
            </div> 
        </select>-->
        <div class="mb-3">
            <label  class="col-sm-2 col-form-label">Card name</label>
            <input type="text" class="form-control" v-model = "addcardData.Title" placeholder="card name" required />
        </div>
        <div class="mb-3">
            <label  class="col-sm-2 col-form-label">Content</label>
            <input type="text" v-model = "addcardData.Content" class="form-control" rows="3" required />
        </div>
            <label for="date" class="col-sm-2 col-form-label">Date</label>
            <div class="col-5"> 
                <div class="input-group date" data-provide="datepicker">
                    <input type="date" v-model = "addcardData.Deadline" class="form-control" >
                    <div class="input-group-addon">
                        <span class="glyphicon glyphicon-th"></span>
                    </div>
                </div>
            </div>
            <br>
    
    
        <div class="form-check form-switch">
          <input class="form-check-input" type="checkbox" v-model="addcardData.Flag" @click="toggleCheckbox">          <!--<input class="form-check-input" type="hidden" id="flexSwitchCheckChecked" v-model="addcardData.Flag" value = "off">--> 
          <label class="form-check-label" for="flexSwitchCheckChecked">Mark as complete</label>
        </div>
    
        <div class="col-5">
          <router-link to="/about" type="button" class="btn btn-primary">Cancel</router-link>
    &nbsp;
            <button type="submit" @click.prevent="AddCard" class="btn btn-primary">Save</button>
        </div>
    </form>
    </div>
</template>

<script>
export default {
      name: 'createCard',
    data() {
      return {
        addcardData:{
       list:"",
        Title: "",
        Content:"",
        Deadline:"",
        Flag:false
      },
      get_list:{}
    };
    },
    async created(){
    this.addcardData.list = this.$route.params.name
    },
    /*async mounted() {
    await fetch("http://localhost:5000/api/allList",
    {mode: 'cors',
    headers:{
      'Content-Type': 'application/json',
      'Authentication-Token':localStorage.getItem('auth-token')
    }}) 
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        //this.name = data["current"];
        this.get_list = data
        console.log('dict',this.get_list)
      });},*/
    methods: {
      toggleCheckbox() {
      this.checkbox = !this.checkbox
      //this.$emit('setCheckboxVal', this.checkbox)
    },
     async AddCard() {
    console.log("msg",this.addcardData)
    await fetch('http://localhost:5000/api/'+this.addcardData.list+'/createcard',
    {mode: 'cors',
    method: 'POST',
    headers: { 'Content-Type': 'application/json' ,
    'Authentication-Token':localStorage.getItem('auth-token')},
    body: JSON.stringify(this.addcardData)
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