<template>
  <div id="list-usuarios">
    <h1>List Apointments</h1>

    <p>
      <router-link :to="{ name: 'create' }" class="btn btn-primary"
        >Create Usuário</router-link
      >
    </p>
    <table class="table table-hover">
      <thead>
        <tr>
          <td>ID</td>
          <td>Titulo</td>
          <td>Detalhes</td>
          <td>Inicio</td>
          <td>Final</td>
          <td>Cor</td>
        </tr>
      </thead>

      <tbody>
        <tr v-for='appoitment in appoitments' v-bind:key='appoitment'>
          <td>{{ appoitment._id['$oid'] }}</td>
          <td>{{ appoitment.Titulo }}</td>
          <td>{{ appoitment.Detalhes }}</td>
          <td>{{ appoitment.Inicio }}</td>
          <td>{{ appoitment.Final }}</td>
          <td>{{ appoitment.Cor }}</td>
          
          <td>
            <router-link
              :to="{ name: 'update', params: { id: appoitment._id['$oid'] } }"
              class="btn btn-primary"
              >Update</router-link
            >
            <router-link
              :to="{ name: 'delete', params: { id: appoitment._id['$oid'] } }"
              class="btn btn-danger"
              >Delete</router-link
            >
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data () {
    return {
      appoitments: []
    }
  },

  created: function () {
    this.fetchUsuarioData()
  },

  methods: {
    fetchUsuarioData: function () {
      this.$http.get('http://localhost:5000/').then(
        (response) => {
          this.appoitments = response.body
        }
      )
    let evento = this.appoitments[0]
    alert(evento)
    }

  }
}
</script>