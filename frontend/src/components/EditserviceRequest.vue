<template>
    <div class="container">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Customer Dashboard</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link class="nav-link active" to="/customer_dashboard">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/customer_dashboard/search">Search</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/summary">Summary</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/logout">Logout</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  
    <div class="container mt-5">
      <h2>Edit Service Request in {{ serviceRequest.service_name }}</h2>
      <form @submit.prevent="updateServiceRequest">
        <div class="form-group">
          <label for="service_name">Service Name:</label>
          <input type="text" class="form-control" id="service_name" v-model="serviceRequest.service_name" readonly>
        </div>
        <div class="form-group">
          <label for="service_professional">Service Professional:</label>
          <input type="text" class="form-control" id="service_professional" v-model="serviceRequest.service_professional" readonly>
        </div>
        <div class="form-group">
          <label for="description">Description:</label>
          <textarea class="form-control" id="description" v-model="serviceRequest.description" rows="5"></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Update Request</button>
      </form>
    </div>
</div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        serviceRequest: {
        //   id: this.$route.params.id, // Get request ID from route params
          service_name: "",
          service_professional: "",
          description: ""
        }
      };
    },
    mounted() {
      this.fetchServiceRequest();
    },
    methods: {
      async fetchServiceRequest() {
        try {
          const response = await fetch(`/api/customer_dashboard/service_request/${this.$route.params.requestId}`,{
            method: "GET",
            headers: { 
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("customerToken")}`
            }
          });
          if (!response.ok) {
            throw new Error("Failed to fetch data");
          }
          const data = await response.json();
          this.serviceRequest.service_name = data.service_name;
          this.serviceRequest.service_professional = data.service_professional;
          this.serviceRequest.description = data.description;
        } catch (error) {
          console.error("Error fetching service request:", error);
        }
      },
      async updateServiceRequest() {
        try {
          const response = await fetch(`/api/customer_dashboard/edit_service_request/${this.$route.params.requestId}`, {
            method: "PUT",
            headers: { 
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("customerToken")}`
            },
            body: JSON.stringify({ description: this.serviceRequest.description })
          });
          if (!response.ok) {
            throw new Error("Failed to update request");
          }
          alert("Service request updated successfully!");
          this.$router.push("/customer-dashboard")

        } catch (error) {
          console.error("Error updating service request:", error);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .container {
    max-width: 600px;
  }
  </style>