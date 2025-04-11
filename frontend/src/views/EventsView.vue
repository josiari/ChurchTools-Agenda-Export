<template>
    <div class="container">
      <div class="row">
        <div class="col">
          <h1>Events</h1>
          <hr><br><br>
          <table class="table table-hover">
            <thead>
              <tr>
                <th scope="col" class="text-center align-middle">ID</th>
                <th scope="col" class="text-center align-middle">Name</th>
                <th scope="col" class="text-center align-middle">Date</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(event, index) in events" :key="index">
                <td class="text-center align-middle">{{ event.id }}</td>
                <td class="text-center align-middle">{{ event.name }}</td>
                <td class="text-center align-middle">{{ event.date }}</td>        
                <td>
                    <button type="button" class="btn btn-primary btn-sm" @click="exportAgenda(event)">Export</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </template>

<script>
import axios from 'axios';
import {saveAs} from 'file-saver';

export default {
  data() {
    return {
      events: [],
    };
  },
  methods: {
    async getEvents() {
      const path = 'http://localhost:5001/events';
      axios.get(path)
        .then((res) => {
          this.events = res.data.data;
        })
        .catch((error) => {
          if (error.response?.status === 401) {
            console.error('You need to be logged in to see the events');
            this.$router.push('/login');
          }
          console.error(error);
        });
    },
    async exportAgenda(event) {
      const path = `http://localhost:5001/events/${event.id}/agenda`;
      axios.get(path, { responseType: 'blob' })
        .then((response) => {
          saveAs(response.data, `agenda_${event.date}.docx`);
        })
        .catch((error) => {
          if (error.response?.status === 404) {
            alert('Agenda not found for this event');
          }
          console.error(error);
        });
    },
  },
  created() {
    this.getEvents();
  },
};
</script>