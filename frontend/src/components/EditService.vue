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
              <router-link class="nav-link" to="/summary">Summary</router-link>
            </li>
            <li class="nav-item">
              <a class="nav-link" @click="logout">Logout</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Edit Service Form -->
    <div class="container mt-5">
      <h1 class="text-center">Edit Service</h1>

      <!-- Show loading spinner while fetching data -->
      <div v-if="loading" class="text-center">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <!-- Form only appears when data is fully loaded -->
      <form v-if="!loading" @submit.prevent="updateService">
        <div class="mb-3">
          <label for="service_name" class="form-label">Service Name</label>
          <input v-model="service.service_name" type="text" class="form-control" id="service_name" required />
        </div>
        <div class="mb-3">
          <label for="service_description" class="form-label">Service Description</label>
          <textarea v-model="service.service_description" class="form-control" id="service_description" required></textarea>
        </div>
        <div class="mb-3">
          <label for="base_price" class="form-label">Base Price</label>
          <input v-model="service.base_price" type="number" class="form-control" id="base_price" required />
        </div>
        <div class="mb-3">
          <label for="time_required" class="form-label">Time Required</label>
          <input v-model="service.time_required" type="text" class="form-control" id="time_required" required />
        </div>
        <button type="submit" class="btn btn-primary">Update Service</button>
      </form>

      <!-- Success Message -->
      <p v-if="message" class="alert alert-success mt-3">{{ message }}</p>
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
        time_required: "",
      },
      message: "",
      loading: true, // Added loading state
    };
  },
  mounted() {
    this.fetchService();
  },
  watch: {
    // Watch for route changes (e.g., navigating to a different service ID)
    "$route.params.id": function () {
      this.fetchService();
    },
  },
  methods: {
    async fetchService() {
      this.loading = true; // Show loading indicator
      try {
        const serviceId = this.$route.params.id;
        const response = await fetch(`/api/services/${serviceId}`);
        if (!response.ok) throw new Error("Failed to fetch service details");
        this.service = await response.json();
      } catch (error) {
        console.error("Error fetching service:", error);
      } finally {
        this.loading = false; // Hide loading indicator after data fetch
      }
    },
    async updateService() {
      try {
        const serviceId = this.$route.params.id;
        const response = await fetch(`/api/services/${serviceId}`, {
          method: "PUT",
          headers: {
            "Authorization": `Bearer ${localStorage.getItem("adminToken")}`,
            "Content-Type": "application/json",
            
          },
          body: JSON.stringify(this.service),
        });

        if (response.ok) {
          this.message = "Service updated successfully!";
          setTimeout(() => {
            this.$router.push("/admin-dashboard");
          }, 1500);
        } else {
          throw new Error("Error updating service");
        }
      } catch (error) {
        console.error("Error updating service:", error);
        alert("Failed to update service. Please try again.");
      }
    },
    logout() {
      localStorage.removeItem("adminToken");
      this.$router.push("/");
    },
  },
};
</script>
