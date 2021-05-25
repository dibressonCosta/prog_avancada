<template>
  <v-app>
   <v-main>
     <Agenda></Agenda>
   </v-main>
  </v-app>
</template>

<script>
import Agenda from './components/Agenda.vue';

export default {
  name: 'App',

  components: {
    Agenda,
  },

  data: () => ({
    //
  }),
};
</script>
