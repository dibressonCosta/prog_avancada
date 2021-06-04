
<template>
  <section class="section-container">
    <v-row class="signin">
      <v-col cols="8" class="left">
        <h1>Trabalho de Progamação Avançada</h1>
      </v-col>
      <v-col cols="4" class="right">
        <h2>Cadastre-se</h2>
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
                required
                outlined
                dense
                dark
                filled
                type="password"
              ></v-text-field>
              <v-text-field
                v-model="password_conf"
                label="Confirme a senha"
                required
                outlined
                dense
                dark
                filled
                type = "password"
              ></v-text-field>

            <div class="text-center">
              <v-btn class="signin-btn" type="submit" rounded color="white" dark>
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
    name: "",
    password_conf: null,
  }),

  methods: {
    async submit() {
      var user = {};
      user.email = this.email
      user.senha = this.password
      console.log(user)
      await axios.post("http://localhost:5000/registro", user).then(
        (response) => {
          console.log(response);
          this.email = null;
          this.password = null;
          this.password_conf = null;
          alert(response.data["mensagem"]);
          this.$router.push("/login")
        },
        (response) => {
          alert(response.data["mensagem"]);
        }
      );
    },
  },
};
</script>

