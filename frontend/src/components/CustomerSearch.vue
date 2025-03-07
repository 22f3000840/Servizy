<template>
    <div>
      <!-- Navbar -->
      <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container-fluid">
          <router-link class="navbar-brand" to="/customer-dashboard">RWU-Customer {{ customerName }}</router-link>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
              <li class="nav-item"><router-link class="nav-link active" to="/customer-dashboard">Home</router-link></li>
              <li class="nav-item"><router-link class="nav-link" to="/customer-dashboard/search">Search</router-link></li>
              <li class="nav-item"><a class="nav-link" href="#" @click="logout">Logout</a></li>
            </ul>
          </div>
        </div>
      </nav>
  
      <!-- Search Form -->
      <div class="container mt-3">
        <form @submit.prevent="searchServices">
          <div class="form-row">
            <div class="col-auto">
              <select class="form-control" v-model="searchType">
                <option value="pincode">Pincode</option>
                <option value="service_name">Service Name</option>
                <option value="address">Address</option>
              </select>
            </div>
            <div class="col-auto">
              <input type="text" class="form-control" v-model="searchQuery" placeholder="Your query">
            </div>
            <div class="col-auto">
              <button type="submit" class="btn btn-primary">Search</button>
            </div>
          </div>
        </form>
        <button class="btn btn-info mt-2" @click="resetSearch">Reset</button>
      </div>
  
      <hr>
  
      <!-- Service List -->
      <div v-if="services.length > 0" class="container">
        <h2>All Services</h2>
        <table class="table">
          <thead>
            <tr>
              <th>Service Name</th>
              <th>Description</th>
              <th>Base Price</th>
              <th>Time Required</th>
              <th>Service Professional</th>
              <th>Rating</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="service in services" :key="service.id">
              <td>{{ service.service_name }}</td>
              <td>{{ service.description }}</td>
              <td>{{ service.base_price }}</td>
              <td>{{ service.time_required }}</td>
              <td>
                <span v-for="professional in service.service_professionals" :key="professional.id">
                  {{ professional.username }}<br>
                </span>
              </td>
              <td>
                <span v-for="professional in service.service_professionals" :key="professional.id">
                  {{ professional.avg_rating || "N/A" }}<br>
                </span>
              </td>
              <!-- <td>
                <span v-for="professional in service.service_professionals" :key="professional.id">
                  <router-link :to="'/customer-dashboard/sp_profile/' + professional.id">View Profile</router-link><br>
                </span>
              </td> -->
            </tr>
          </tbody>
        </table>
      </div>
      <p v-else>No services found.</p>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        customerName: "",
        searchType: "pincode",
        searchQuery: "",
        services: []
      };
    },
    mounted() {
      this.fetchServices();
    },
    methods: {
      async fetchServices() {
        try {
          const token = localStorage.getItem("customerToken");
          const response = await fetch(`/api/customer_dashboard/search`, {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              "Authorization": "Bearer " + token
            }
          });
  
          if (!response.ok) throw new Error("Failed to fetch services");
  
          const data = await response.json();
          this.customerName = data.customer_name;
          this.services = data.services || [];
        } catch (error) {
          console.error("Error fetching services:", error);
        }
      },
      async searchServices() {
        try {
          const token = localStorage.getItem("customerToken");
          const response = await fetch(`/api/customer_dashboard/search?search_type=${this.searchType}&search_query=${this.searchQuery}`, {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              "Authorization": "Bearer " + token
            }
          });
  
          if (!response.ok) throw new Error("Search request failed");
  
          const data = await response.json();
          this.services = data.services || [];
        } catch (error) {
          console.error("Error searching services:", error);
        }
      },
      resetSearch() {
        this.searchType = "pincode";
        this.searchQuery = "";
        this.fetchServices();
      },
      logout() {
        localStorage.removeItem("customerToken");
        this.$router.push("/");
      }
    }
  };
  </script>
  
  <style scoped>
  .container {
    margin-top: 20px;
  }
  </style>
  