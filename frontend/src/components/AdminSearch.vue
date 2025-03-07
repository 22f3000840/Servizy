<template>
    <div>
      <!-- Navbar -->
      <nav class="navbar navbar-expand-lg navbar-dark bg-danger">
        <div class="container-fluid">
          <a class="navbar-brand" href="#">Admin Dashboard</a>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
              <li class="nav-item">
                <router-link to="/admin-dashboard" class="nav-link active">Home</router-link>
              </li>
              <li class="nav-item">
                <router-link to="/admin-dashboard/search" class="nav-link">Search</router-link>
              </li>
              <li class="nav-item">
                <a class="nav-link" aria-current="page" @click="logout">Logout</a>
              </li>
            </ul>
          </div>
        </div>
      </nav>
  
      <!-- Search Form -->
      <div class="container mt-3">
        <form @submit.prevent="search">
          <div class="row">
            <div class="col-auto">
              <select v-model="searchType" class="form-control">
                <option value="service">Service</option>
                <option value="user">User</option>
              </select>
            </div>
            <div class="col-auto">
              <input v-model="searchQuery" type="text" class="form-control" placeholder="Your query" />
            </div>
            <div class="col-auto">
              <button type="submit" class="btn btn-primary">Search</button>
            </div>
            <div class="col-auto">
              <button type="button" class="btn btn-info" @click="resetSearch">Reset</button>
            </div>
          </div>
        </form>
      </div>
      
      <hr />
  
      <!-- User Results -->
      <div v-if="users.length" class="container">
        <h2>All Users</h2>
        <table class="table">
          <thead>
            <tr>
              <th>Username</th>
              <th>Address</th>
              <th>Pincode</th>
              <th>Role</th>
              <th>Average Rating</th>
              <th>Rating Count</th>
              <!-- <th>ServiceProfessional File</th> -->
              <th>Service ID</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.username }}</td>
              <td>{{ user.address }}</td>
              <td>{{ user.pincode }}</td>
              <td>{{ user.role }}</td>
              <td>{{ user.avg_rating }}</td>
              <td>{{ user.rating_count }}</td>
              <!-- <td>{{ user.sp_file }}</td> -->
              <td>{{ user.service_id }}</td>
              <td>
                <button
                  class="btn btn-sm"
                  :class="user.is_flagged ? 'btn-success' : 'btn-danger'"
                  @click="toggleBlockUser(user.id)"
                  >
                  {{ user.is_flagged ? "Unblock" : "Block" }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else-if="searchTriggered" class="alert alert-warning">
        <h2>No users found</h2>
      </div>
  
      <!-- Service Results -->
      <div v-if="services.length" class="container">
        <h2>All Services</h2>
        <table class="table">
          <thead>
            <tr>
              <th>Service Name</th>
              <th>Service Description</th>
              <th>Service Base Price</th>
              <th>Time Required</th>
              <th>ServiceProfessional Name</th>
              <th>ServiceProfessional Rating</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="service in services" :key="service.id">
              <td>{{ service.service_name }}</td>
              <td>{{ service.service_description }}</td>
              <td>{{ service.base_price }}</td>
              <td>{{ service.time_required }}</td>
              <td>
                <span v-for="professional in service.service_professionals" :key="professional.id">
                  {{ professional.username }}<br />
                </span>
              </td>
              <td>
                <span v-for="professional in service.service_professionals" :key="professional.id">
                  {{ professional.avg_rating }}<br />
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else-if="searchTriggered" class="alert alert-warning">
        <h2>No services found</h2>
      </div>

    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        searchType: "service",
        searchQuery: "",
        users: [],
        services: [],
        searchTriggered: false
      };
    },
    methods: {
      async search() {
        this.searchTriggered = true;
        try {
          const response = await fetch(`/api/admin_dashboard/search?search_type=${this.searchType}&search_query=${this.searchQuery}`, {
            headers: {
              "Authorization": `Bearer ${localStorage.getItem("adminToken")}`,
              "Content-Type": "application/json",
            }
          });
          if (!response.ok) throw new Error("Failed to fetch data");
  
          const data = await response.json();
          this.users = data.users || [];
          this.services = data.services || [];
        } catch (error) {
          console.error("Error fetching search results:", error);
        }
      },
      async toggleBlockUser(userId) {
    try {
      const response = await fetch(`/api/admin_dashboard/block_user/${userId}`, {
        method: "PATCH",
        headers: {
          "Authorization": `Bearer ${localStorage.getItem("adminToken")}`,
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) throw new Error("Failed to update user status");

      const data = await response.json();
      alert(data.message);

      // Update the user's status in the local users array
      this.users = this.users.map(user => {
        if (user.id === userId) {
          return { ...user, is_flagged: !user.is_flagged }; // Toggle the is_flagged status
        }
        return user;
      });
    } catch (error) {
      console.error("Error toggling block status:", error);
      alert("Failed to update user status. Please try again.");
    }
  },
      resetSearch() {
        this.searchQuery = "";
        this.users = [];
        this.services = [];
        this.searchTriggered = false;
      },
      async logout() {
        localStorage.removeItem("adminToken");
        this.$router.push("/");
      }
    }
  };
  </script>
  