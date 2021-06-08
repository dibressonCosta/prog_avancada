<template>
  <v-row class="fill-height">
    <v-col>
      <v-sheet height="64">
        <v-toolbar flat>
          <v-btn outlined class="mr-4" color="grey darken-2" @click="setToday">
            Hoje
          </v-btn>
          <v-btn color="red lighten-3" dark @click.stop="dialog = true">
            Novo Evento
          </v-btn>
          <v-btn fab text small color="grey darken-2" @click="prev">
            <v-icon small> mdi-chevron-left </v-icon>
          </v-btn>
          <v-btn
            fab
            text
            small
            color="grey darken-2"
            @click="next"
            class="mr-4"
          >
            <v-icon small> mdi-chevron-right </v-icon>
          </v-btn>
          <v-toolbar-title v-if="$refs.calendar">
            {{ $refs.calendar.title }}
          </v-toolbar-title>
          <v-spacer></v-spacer>
          <v-menu bottom right>
            <template v-slot:activator="{ on, attrs }">
              <v-btn outlined color="grey darken-2" v-bind="attrs" v-on="on">
                <span>{{ typeToLabel[type] }}</span>
                <v-icon right> mdi-menu-down </v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item @click="type = 'day'">
                <v-list-item-title>Dia</v-list-item-title>
              </v-list-item>
              <v-list-item @click="type = 'week'">
                <v-list-item-title>Semana</v-list-item-title>
              </v-list-item>
              <v-list-item @click="type = 'month'">
                <v-list-item-title>Mês</v-list-item-title>
              </v-list-item>
              <v-list-item @click="type = '4day'">
                <v-list-item-title>4 dias</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
          <v-btn color="red lighten-3" style="margin-left: 10px;" dark @click.prevent="sair()">
            Sair
          </v-btn>
        </v-toolbar>
      </v-sheet>
      <!-- adicionar evento -->

      <v-dialog v-model="dialog" max-width="500">
        <v-card>
          <v-container>
            <v-form @submit.prevent="addEvent">
              <v-text-field
                v-model="name"
                type="text"
                label="Nome do evento (Obrigatório)"
              >
              </v-text-field>
              <v-text-field v-model="details" type="text" label="detalhes">
              </v-text-field>
              <v-text-field
                v-model="start"
                type="date"
                label="Início (Obrigatório)"
              >
              </v-text-field>
              <v-text-field
                v-model="end"
                type="date"
                label="Final (Obrigatório)"
              >
              </v-text-field>
              <v-text-field
                v-model="color"
                type="color"
                label="cor (click para abrir o menu)"
              >
              </v-text-field>
              <v-btn
                type="submit"
                :color="color"
                class="mr-4"
                @click.stop="dialog = false"
              >
                Criar Evento
              </v-btn>
              <v-btn text color="secondary" @click="dialog = false">
                Fechar
              </v-btn>
            </v-form>
          </v-container>
        </v-card>
      </v-dialog>

      <v-sheet height="700">
        <v-calendar
          ref="calendar"
          v-model="focus"
          color="red lighten-3"
          locale="pt"
          :events="events"
          :event-color="getEventColor"
          :type="type"
          @click:event="showEvent"
          @click:more="viewDay"
          @click:date="viewDay"
        ></v-calendar>
        <v-menu
          v-model="selectedOpen"
          :close-on-content-click="false"
          :activator="selectedElement"
          offset-x
        >
          <v-card color="grey lighten-4" min-width="350px" flat>
            <v-toolbar :color="selectedEvent.color" dark>
              <v-btn @click.prevent="deleteEvent(selectedEvent)" icon>
                <v-icon>mdi-delete</v-icon>
              </v-btn>
              <v-toolbar-title v-html="selectedEvent.name"></v-toolbar-title>
              <v-spacer></v-spacer>
            </v-toolbar>
            <v-card-text>
              <form v-if="currentlyEditing !== selectedEvent.id">
                {{ selectedEvent.details }}
              </form>
              <form v-else>
                <textarea-autosize
                  v-model="selectedEvent.details"
                  type="text"
                  style="width: 100%"
                  :min-height="100"
                  placeholder="Adicionar nota"
                ></textarea-autosize>
              </form>
            </v-card-text>
            <v-card-actions>
              <v-btn text color="secondary" @click="selectedOpen = false">
                Cancelar
              </v-btn>
              <v-btn
                text
                color="secondary"
                v-if="currentlyEditing !== selectedEvent.id"
                @click.prevent="editEvent(selectedEvent)"
              >
                Editar
              </v-btn>
              <v-btn
                text
                color="secondary"
                v-else
                @click.prevent="updateEvent(selectedEvent)"
              >
                Salvar
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-menu>
      </v-sheet>
    </v-col>
  </v-row>
</template>

<script>
import axios from "axios";
axios.defaults.headers.common["Content-Type"] = "application/json";
axios.defaults.headers.common["Access-Control-Allow-Origin"] = "*";
axios.defaults.headers.common = {'Authorization': `bearer ${localStorage.getItem('token')}`}

export default {
  data: () => ({
    today: new Date().toISOString().substr(0, 10),
    focus: new Date().toISOString().substr(0, 10),
    type: "month",
    typeToLabel: {
      month: "Mês",
      week: "Semana",
      day: "Dia",
      "4day": "4 dias",
    },
    name: null,
    details: null,
    start: null,
    end: null,
    color: "#6593A6",
    currentlyEditing: null,
    selectedEvent: {},
    selectedElement: null,
    selectedOpen: false,
    events: [],
    dialog: false,
  }),
  created: function () {
    this.fetchEventData();
  },

  methods: {
    fetchEventData: async function () {
      var user = {};
      user.id = localStorage.getItem('id');
      await axios.post("http://localhost:5000/index", user).then((response) => {
        this.events = response.data;

      });
    },
    sair(){
      localStorage.clear();
      this.$router.push("/login");
    },
    async addEvent() {
      var ev = {};
      ev.name = this.name;
      ev.details = this.details;
      ev.start = this.start;
      ev.end = this.end;
      ev.color = this.color;
      ev.userId = localStorage.getItem('id');
      console.log(ev);
      await axios.post("http://localhost:5000/event", ev).then(
        (response) => {
          console.log(response);
          this.name = null;
          this.details = null;
          this.start = null;
          this.end = null;
          this.color = "#1976d2";
          this.fetchEventData();
        },
        (response) => {
          alert(response.data["mensagem"]);
        }
      );
    },
    async updateEvent(evento) {
      var ev = {};
      ev.id = evento._id.$oid;
      ev.name = evento.name;
      ev.details = evento.details;
      ev.start = evento.start;
      ev.end = evento.end;
      ev.color = evento.color;
      await axios.put("http://localhost:5000/event", ev).then(
        (response) => {
          console.log(response);
        },
        (response) => {
          alert(response.data["mensagem"]);
        }
      );
    },
    async deleteEvent(evento) {
      var ev = {};
      ev.id = evento._id.$oid;
      await axios.delete("http://localhost:5000/event", { data: ev }).then(
        (response) => {
          this.selectedOpen = false;
          this.fetchEventData();
          console.log(response);
        },
        (response) => {
          alert(response.data["mensagem"]);
        }
      );
    },
    viewDay({ date }) {
      this.focus = date;
      this.type = "day";
    },
    getEventColor(event) {
      return event.color;
    },
    setToday() {
      this.focus = "";
    },
    prev() {
      this.$refs.calendar.prev();
    },
    next() {
      this.$refs.calendar.next();
    },
    editEvent(evento) {
      this.currentlyEditing = evento.id;
    },
    showEvent({ nativeEvent, event }) {
      const open = () => {
        this.selectedEvent = event;
        this.selectedElement = nativeEvent.target;
        requestAnimationFrame(() =>
          requestAnimationFrame(() => (this.selectedOpen = true))
        );
      };

      if (this.selectedOpen) {
        this.selectedOpen = false;
        requestAnimationFrame(() => requestAnimationFrame(() => open()));
      } else {
        open();
      }

      nativeEvent.stopPropagation();
    },
  },
};
</script>
