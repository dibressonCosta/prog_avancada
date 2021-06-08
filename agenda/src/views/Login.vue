
<template>
  <section class="section-container">
    <v-row class="signin">
      <v-col cols="8" class="left">
        <h1>Trabalho de Progamação Avançada</h1>
      </v-col>
      <v-col cols="4" class="right">
        <h2>LOGIN</h2>
        <v-form @submit.prevent="submit">
          <v-text-field
            v-model="email"
            label="Email"
            required
            outlined
            dark
            filled
            dense
          ></v-text-field>
          <v-text-field
            v-model="password"
            label="Senha"
            :append-icon="showPass ? 'mdi-eye' : 'mdi-eye-off'"
            @click:append="showPass = !showPass"
            required
            outlined
            dense
            dark
            filled
            :type="showPass ? 'text' : 'password'"
          ></v-text-field>
          <div class="text-center">
            <v-btn class="signin-btn" type="submit" rounded color="white" dark>
              Entrar
            </v-btn>
          </div>
          <div class="text-center" style="padding-top: 10px">
            <v-btn
              class="signin-btn"
              type="button"
              href="/cadastro"
              rounded
              color="white"
              dark
            >
              Cadastrar
            </v-btn>
          </div>
        </v-form>
      </v-col>
    </v-row>
  </section>
</template>


<script>
import axios from "axios";
axios.defaults.headers.common["Content-Type"] = "application/json";
axios.defaults.headers.common["Access-Control-Allow-Origin"] = "*";

export default {
  data: () => ({
    email: "",
    password: null,
    showPass: false,
  }),
  methods: {
    async submit() {
      var user = {};
      user.email = this.email;
      user.senha = this.password;
      await axios.post("http://localhost:5000/login", user).then(
        (response) => {
          this.email = null;
          this.password = null;
          if (response.status == 200) {
            console.log(response.data.token)
            localStorage.setItem("token", response.data.token);
            localStorage.setItem("email", user.email);
            localStorage.setItem("id", response.data.result[0]._id.$oid);
            this.$router.push("/");
          }
        },
        (response) => {
         this.$swal("Dados inválidos");
         console.log(response)
        }
      );
    },
  },
};
</script>

