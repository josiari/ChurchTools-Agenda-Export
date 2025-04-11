<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Login</h1>
        <hr><br><br>
        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label for="username">Username</label>
            <input
              type="text"
              id="username"
              class="form-control"
              v-model="username"
              placeholder="Enter your username"
              required
            />
          </div>
          <div class="form-group">
            <label for="password">Password</label>
            <input
              type="password"
              id="password"
              class="form-control"
              v-model="password"
              placeholder="Enter your password"
              required
            />
          </div>
          <button type="submit" class="btn btn-primary mt-3">Login</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    handleLogin() {
      if (this.username && this.password) {
        const path = 'http://localhost:5001/login';
        const payload = {
          username: this.username,
          password: this.password,
        };
        axios.post(path, payload)
          .then((response) => {
            if (response.status === 200) {
              console.log('Login successful:', response.data);
              this.$router.push('/');
            } else {
              console.error('Login failed:', response.data);
            }
          })
          .catch((error) => {
            console.error('Error during login:', error);
          });
      } else {
        console.error('Please fill in both fields.');
      }
    },
  },
};
</script>

<style scoped>
/* Add any custom styles here */
</style>