
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
                v-model="nome"
                label="Nome de usuário"
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
          </v-form>
      </v-col>
    </v-row>
  </section>
</template>


<script>

export default {
  data: () => ({
    email: "",
    password: null,
    showPass: false,
  }),
  computed: {
    params() {
      return {
        email: this.email,
        password: this.password,
      };
    },
  },
  methods: {
    async submit() {
      const valid = await this.$refs.observer.validate();
      if (valid) {
        this.login(this.params); // action to login
      }
    },
    clear() {
      // you can use this method to clear login form
      this.email = "";
      this.password = null;
      this.$refs.observer.reset();
    },
  },
};
</script>

