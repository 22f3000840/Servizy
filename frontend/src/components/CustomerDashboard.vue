<template>
    <div>
      <!-- Navbar -->
      <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container-fluid">
          <a class="navbar-brand" href="#">Customer Dashboard</a>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav me-auto">
              <li class="nav-item">
                <router-link class="nav-link active" to="/customer-dashboard">Home</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/customer-dashboard/search">Search</router-link>
              </li>
              <li class="nav-item">
                <a class="nav-link" aria-current="page" @click="logout">Logout</a>
              </li>
            </ul>
            <ul class="navbar-nav ms-auto">
              <li class="nav-item">
                <span class="nav-link">{{ customerName }}</span>
              </li>
            </ul>
          </div>
        </div>
      </nav>
  
      <div class="container mt-4">
        <!-- Available Services -->
        <h2>Available Services</h2>
        <div class="row row-cols-1 row-cols-md-3 g-4">
          <div v-for="service in services" :key="service.id" class="col">
            <div class="card h-100">
              <div class="card-body">
                <h5 class="card-title">{{ service.service_name }}</h5>
                <p class="card-text">{{ service.service_description }}</p>
                <router-link :to="'/customer-dashboard/create-service-request/' + service.id" class="btn btn-primary" @click="createServiceRequest(service.id)">Create New Request</router-link>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Service History -->
        <h2 class="mt-4">Service History</h2>
        <table v-if="serviceHistory.length > 0" class="table table-striped">
          <thead>
            <tr>
              <th>Service Name</th>
              <th>Description</th>
              <th>Service Professional</th>
              <th>Request Type</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in serviceHistory" :key="request.id">
              <td>{{ request.service_name ?? "Unknown service" }}</td>
              <td>{{ request.description }}</td>
              <td>{{ request.service_professional}}</td>
              <td>{{ request.request_type }}</td>
              <td>{{ request.status }}</td>
              <td>
                <button v-if="request.status === 'accepted'" class="btn btn-success" @click="closeRequest(request.request_id)">Close Request</button>
                <button v-else-if="request.status === 'pending'" class="btn btn-warning me-2" @click="editRequest(request.request_id)">Edit Request</button>
                <button v-if="request.status === 'pending'" class="btn btn-danger" @click="deleteRequest(request.request_id)">Cancel Request</button>
              </td>
            </tr>
          </tbody>
        </table>
        <p v-else>No service history yet</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        customerName: "",
        services: [],
        serviceHistory: [],
      };
    },
    mounted() {
      this.fetchData();
    },
    methods: {
      async fetchData() {
        try {
          const response = await fetch("/api/customer_dashboard", {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              "Authorization": "Bearer " + localStorage.getItem("customerToken")
            }
          });
          const data = await response.json();
          this.customerName = data.customer_name;
          this.services = data.available_services || [];
          this.serviceHistory = data.service_history || [];
        } catch (error) {
          console.error("Error fetching data:", error);
        }
      },
      async createServiceRequest(serviceId) {
        try {
          await fetch(`/api/customer_dashboard/create_service_request/${serviceId}`, { method: "POST" });
          this.fetchData(); // Refresh data
        } catch (error) {
          console.error("Error creating request:", error);
        }
      },
        async closeRequest(requestId) {
    try {
      const response = await fetch(`/api/customer_dashboard/close_request/${requestId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + localStorage.getItem("customerToken"),
        },
        body: JSON.stringify({}) // Initially no review/rating is provided
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Error closing request: ${response.status}, ${errorText}`);
      }

      // Redirect to review-rating page
      this.$router.push(`/customer-dashboard/review-rating/${requestId}`);
    } catch (error) {
      console.error("Error closing request:", error);
      alert("Failed to close request. Please try again.");
    }
  },


  async editRequest(requestId) {
  try {
    // Redirect to the edit request page with the request ID
    this.$router.push(`/customer-dashboard/edit-service-request/${requestId}`);
  } catch (error) {
    console.error("Error navigating to edit request:", error);
    alert("Failed to navigate to edit request. Please try again.");
  }
},
      async deleteRequest(requestId) {
        try {
          const response=await fetch(`/api/customer_dashboard/cancel_service_request/${requestId}`, {
             method: "DELETE",
             headers: {
               "Content-Type": "application/json",
               "Authorization": "Bearer " + localStorage.getItem("customerToken"),
             },
             });
            if (response.ok) {
              const result=await response.json();
              alert(result.message);
              this.fetchData();
              this.$router.push('/customer-dashboard');
            }else {
              alert('error deleting request');
            }
        } catch (error) {
          console.error("Error deleting request:", error);
        }
      },
      async logout(){
        localStorage.removeItem("customerToken");
        this.$router.push("/");
      }
    }
  };
  </script>
  
  <style>
  .container {
    margin-top: 20px;
  }
  </style>
  