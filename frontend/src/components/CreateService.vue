<template>
    <div>
      <!-- Navbar -->
      <nav class="navbar navbar-expand-lg navbar-dark bg-danger">
        <div class="container-fluid">
          <a class="navbar-brand" href="#">Admin Dashboard</a>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
              <li class="nav-item">
                <router-link class="nav-link active" to="/admin-dashboard">Home</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/search">Search</router-link>
              </li>
              <li class="nav-item">
                <a class="nav-link" aria-current="page" @click="exportdata">Export CSV</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" aria-current="page" @click="logout">Logout</a>
              </li>
            </ul>
          </div>
        </div>
      </nav>
  
      <!-- Create Service Form -->
      <div class="container mt-5">
        <h1 class="text-center">Create Service</h1>
        <form @submit.prevent="createService">
          <div class="mb-3">
            <label for="service_name" class="form-label">Service Name</label>
            <input type="text" class="form-control" id="service_name" v-model="service.service_name" required>
          </div>
          <div class="mb-3">
            <label for="service_description" class="form-label">Service Description</label>
            <textarea class="form-control" id="service_description" v-model="service.service_description" required></textarea>
          </div>
          <div class="mb-3">
            <label for="base_price" class="form-label">Base Price</label>
            <input type="number" class="form-control" id="base_price" v-model="service.base_price" required>
          </div>
          <div class="mb-3">
            <label for="time_required" class="form-label">Time Required</label>
            <input type="text" class="form-control" id="time_required" v-model="service.time_required" required>
          </div>
          <button type="submit" class="btn btn-primary">Create Service</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        service: {
          service_name: "",
          service_description: "",
          base_price: "",
          time_required: ""
        }
      };
    },
    methods: {
      async createService() {
        try {
          const response = await fetch("/api/services", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${localStorage.getItem("adminToken")}`
            },
            body: JSON.stringify(this.service)
          });
          
          if (response.ok) {
            const result = await response.json();
            alert(result.message);
            this.$router.push("/admin-dashboard");
          } else {
            alert("Error creating service");
          }
        } catch (error) {
          console.error("Error creating service:", error);
        }
      },
      logout() {
        localStorage.removeItem("adminToken");
        this.$router.push("/");
      }
    }
  };
  </script>
  
  <style scoped>
  .container {
    max-width: 600px;
  }
  </style>