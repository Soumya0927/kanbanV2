<template>
   <div class="row row-cols-1 row-cols-md-3 g-4">
    <div
      :key="l"
      v-for="l in Object.keys(lists)"
      class="list px-3 py-4 d-flex flex-column gap-1 position-relative"
    >
<div class="card-deck">
<div class="card" style="width: 25rem; height:20rem" >

  <div class="card-header"> {{l}}</div>  
  <Bar
        id="my-chart-id"
        :options="chartOptions"
        :data="getData(l)"
      />
  </div></div></div></div>
  <div class="col-5">
          <router-link to="/about" type="button" class="btn btn-primary">Back to dashboard</router-link>
    &nbsp;</div>
</template>

<script>
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
  name: 'BarChart',
  components: { Bar },
  async mounted () {
      this.loaded = false
        const  response  = await fetch('http://localhost:5000/api/summary',
        {mode: 'cors',
        headers:{
      'Content-Type': 'application/json',
      'Authentication-Token':localStorage.getItem('auth-token')
    }})
      const userlist = await  response.json(); 
      this.loaded = true; 
      this.lists = userlist; 
      console.log(userlist)
      console.log(this.lists)
    },
    methods: {
      getData(l){
        return {
            labels: [ 'Completed', 'Incompleted', 'Deadline over'],
            datasets:  [{label: l,
              data: this.lists[l],
            backgroundColor: [
      'rgba(255, 99, 132, 0.5)',
      'rgba(255, 205, 86, 0.5)',
      'rgba(54, 162, 235, 0.5)'],

    borderWidth:2,
    
  }],
             }}},

     

 data() {
   return {
    lists: [],
    chartOptions: {
        responsive: true,
        plugins:{
          legend:{display:false},

        },
        enabled:false,
        scales: {
          y: {stacked: true,
            
               ticks: {
                  min: 0,
                 stepSize: 1,
                  
              }

          }
      
      }
      },
      
     }

}

  }
</script>
<style>
  .chartbox{
    width: 300px;
  }
</style>