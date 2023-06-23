<!--<template>
  <div class="about">
    <h1>This is an about page{{ msg }}</h1>

     </div>
</template>-->
<template><NavBardash />
<p><b style="color:tomato">Hi, {{name}} welcome to kanban app.</b></p>
  <div class="row row-cols-1 row-cols-md-4 ">
  <div v-for="(key) in Object.keys(get_cards)" :key="key" >
    <div class="card-deck">
  
    <div class="dropdown">
      <button class="btn btn-dark dropdown-toggle" type="button"  data-bs-toggle="dropdown" aria-expanded= "true" >
      {{key}}
      </button>
      <ul class="dropdown-menu" >
      <li><router-link class="dropdown-item"  :to="`/${key}/editlist`">Edit</router-link></li>
      <li><a class="dropdown-item" v-on:click=deleteTask(key)>Delete</a></li>
      <li><a class="dropdown-item" v-on:click=download(key)>Export</a></li>
      </ul>
    </div>
  
     <div v-for = "val in get_cards[key]" :key="val">  
    <div class="card border-warning mb-3" style="max-width: 18rem;">
        <div class="card-header">        
           <div class="dropdown">
                    <button class="btn btn-warning dropdown-toggle" type="button"  data-bs-toggle="dropdown" aria-expanded="true" style="--bs-btn-padding-x: 5rem;">
                        {{val['card_title']}}
                    </button>
              <ul class="dropdown-menu">
                <li><router-link class="dropdown-item" :to="`/${val['cid']}/updatecard`">EDIT</router-link></li>
                <li><a class="dropdown-item" v-on:click=deleteCard(val.cid)>DELETE</a></li>  
                <li><a class="dropdown-item" v-on:click=downloadcard(val.cid)>EXPORT</a></li>
              </ul>
            </div>
        </div>
        <div class="card-body"> 
          <!--p v-if="cssAlignement(val['deadline'])"  > Over Due Date</p-->
          <p v-if="val['flag'] == false"  >
            <span style="font-size: small; font-weight: 600; color: red;">Pending</span>
          
          <small><div :style="{ color: due(val) ? 'red' : 'yellow' }">
      {{due(val) ? 'Due date over' : ''}}
    </div></small></p>
          <p v-else >
            <span style="line-height: 0.01em; font-size: small; font-weight: 600; color: green;">Completed</span>
          </p>
      
          <h6 class="card-title">{{val['content']}}</h6>
          
          <!--div :class='due(val)'>Hello simple class</div-->
          <p class="row_class"><small class="text-muted">Deadline : {{val['deadline']}}</small></p>
  
        </div>
    
  
    </div>
   </div>
      <router-link :to="`/${key}/newcard`">
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-plus-circle-fill" viewBox="0 0 16 16">
    <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3v-3z"/>
  </svg></router-link>       
    
    </div>
   </div>
    <router-link to="/createlist">
      <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-plus-circle-fill" viewBox="0 0 16 16">
    <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8.5 4.5a.5.5 0 0 0-1 0v3h-3a.5.5 0 0 0 0 1h3v3a.5.5 0 0 0 1 0v-3h3a.5.5 0 0 0 0-1h-3v-3z"/>
  </svg> </router-link>
  </div>
  </template>
<script>
    import NavBardash from '@/components/NavBardash.vue'

  export default {
  name: "AboutView",
  
  data() {
    return {
      name: "user",
      auth_token : null,
      get_cards: {},
      //todaysDate : new Date()
    };
  },
  components:{
          NavBardash
        },
  computed:{
    
  },
  async created(){
    this.auth_token = localStorage.getItem('auth-token')
    if (!this.auth_token){
      alert('Please login to access this page')
      this.$router.push('/login')
    }
  },
methods:{
  due(val){
    console.log(val['deadline'])
    let date = new Date(val['deadline'])
    console.log(date)
    var todaysDate = new Date();
    console.log(todaysDate)

    if (date < todaysDate){
      return true;
    }
    else{
    return false;
    }
},
  
 async deleteTask(key) {
      console.log(key)
      const sure = confirm('Are you sure?')
      if (sure) {
      await fetch("http://localhost:5000/api/tasks/"+key,
          { mode:'cors',
            method: 'DELETE',
            headers:{
      'Content-Type': 'application/json',
      'Authentication-Token':localStorage.getItem('auth-token')
    }
  },).then(() => {
            alert('Successfully Deleted');
            location.reload();
          })
          .catch((err) => {
            console.log(err.message)
          })
      }
    },
    async deleteCard(id) {
      console.log(id)
      const sure = confirm('Are you sure?')
      if (sure) {
      await fetch("http://localhost:5000/api/card/"+id,
          { mode:'cors',
            method: 'DELETE',
            headers:{
      'Content-Type': 'application/json',
      'Authentication-Token':localStorage.getItem('auth-token')
    }
    },
          )
          .then(() => {
            alert('Successfully Deleted');
            location.reload();
          })
          .catch((err) => {
            console.log(err.message)
          })
      }
    },
    download(key){
     fetch("http://localhost:5000/api/downloadlist/"+key,{
          method: 'GET', 
          mode: 'cors', 
          headers: {
      'Content-Type': 'application/json',
      'Authentication-Token':localStorage.getItem('auth-token')
      }
       }).then( () => {alert("We have received your download request. We will notify you about its status via an email.");})
       .catch( e => console.log(e));
      
    },
    downloadcard(id){
     fetch("http://localhost:5000/api/downloadcard/"+id,{
          method: 'GET', 
          mode: 'cors', 
          headers: {
      'Content-Type': 'application/json',
      'Authentication-Token':localStorage.getItem('auth-token')
      }
       }).then( () => {alert("We have received your download request. We will notify you about its status via an email.");})
       .catch( e => console.log(e));
      
    }
},
  
  async mounted() {
    await fetch("http://localhost:5000/api/users",
    {mode: 'cors',
    headers:{
      'Content-Type': 'application/json',
      'Authentication-Token':localStorage.getItem('auth-token')
    }})
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        this.get_cards = data["result"]
        this.name = data["username"]
        console.log('dict',this.get_cards)
      });
  }};
  //import routes from '../router/index.js'

  </script>
  <style >

</style>