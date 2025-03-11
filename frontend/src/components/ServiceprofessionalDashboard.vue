<template>
    <div>
      <!-- Navbar -->
      <nav class="navbar navbar-expand-lg navbar-dark bg-warning">
        <div class="container-fluid">
          <a class="navbar-brand" href="#">Service Professional Dashboard</a>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
              <li class="nav-item">
                <router-link class="nav-link active" to="/sp_dashboard">Home</router-link>
              </li>
              <li class="nav-item">
                <a class="nav-link" aria-current="page" @click="logout">Logout</a>
              </li>
            </ul>
            <ul class="navbar-nav ms-auto">
              <li class="nav-item">
                <span class="nav-link">{{ spName }}</span>
              </li>
            </ul>
          </div>
        </div>
      </nav>
  
      <div class="container mt-4">
        <!-- Pending Requests Table -->
        <h2>Pending Requests</h2>
        <table v-if="pendingRequests.length > 0" class="table table-striped">
          <thead>
            <tr>
              <th>Customer ID</th>
              <th>Request Type</th>
              <th>Description</th>
              <th>Created At</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in pendingRequests" :key="request.id">
              <td>{{ request.customer_id }}</td>
              <td>{{ request.request_type }}</td>
              <td>{{ request.description }}</td>
              <td>{{ request.date_created }}</td>
              <td>
                <button class="btn btn-success me-2" @click="acceptRequest(request.id)">Accept</button>
                <button class="btn btn-danger" @click="rejectRequest(request.id)">Reject</button>
              </td>
            </tr>
          </tbody>
        </table>
        <p v-else>No pending requests</p>
  
        <!-- Accepted Requests Table -->
              <h2>Accepted Requests</h2>
      <table v-if="acceptedRequests.length > 0" class="table table-striped">
        <thead>
          <tr>
            <th>Customer ID</th>
            <th>Request Type</th>
            <th>Description</th>
            <th>Created At</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in acceptedRequests" :key="request.id">
            <td>{{ request.customer_id }}</td>
            <td>{{ request.request_type }}</td>
            <td>{{ request.description }}</td>
            <td>{{ request.date_created }}</td>
            <td>
              <button class="btn btn-primary" @click="closeRequest(request.id)">Close Request</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>No accepted requests</p>
  
        <!-- Closed Requests Table -->
              <h2>Closed Requests</h2>
      <table v-if="closedRequests.length > 0" class="table table-striped">
        <thead>
          <tr>
            <th>Customer ID</th>
            <th>Request Type</th>
            <th>Status</th>
            <th>Closed At</th>
            <th>Closed By</th> <!-- NEW COLUMN -->
            <th>Rating by Customer</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in closedRequests" :key="request.id">
            <td>{{ request.customer_id }}</td>
            <td>{{ request.request_type }}</td>
            <td>{{ request.status }}</td>
            <td>{{ request.date_closed }}</td>
            <td>
              <span v-if="request.closed_by === 'service_professional'">Service Professional</span>
              <span v-else-if="request.closed_by === 'customer'">Customer</span>
              <span v-else>Unknown</span>
            </td>
            <td>{{ request.rating_by_customer }}/5</td>
          </tr>
        </tbody>
      </table>
      <p v-else>No requests completed yet</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        spName: "",
        pendingRequests: [],
        acceptedRequests: [],
        closedRequests: [],
      };
    },
    mounted() {
      this.fetchData();
    },
    methods: {
      async fetchData() {
        try {
          const response = await fetch("/api/requests_sp",{
            headers: {
              "Authorization": `Bearer ${localStorage.getItem("serviceProfessionalToken")}`,
              "Content-Type": "application/json",
            },
          });
          const data = await response.json();
          this.spName = data.sp_username;
          this.pendingRequests = data.pending_requests || [];
          this.acceptedRequests = data.accepted_requests || [];
          this.closedRequests = data.closed_requests || [];
        } catch (error) {
          console.error("Error fetching data:", error);
        }
      },
      async acceptRequest(requestId) {
  try {
    const response = await fetch(`/api/requests_sp/${requestId}`, {
      method: "PATCH",
      headers: {
        "Authorization": `Bearer ${localStorage.getItem("serviceProfessionalToken")}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ action: "accept" })
    });

    const result = await response.json();
    
    if (response.ok) {
      // Find the request in pendingRequests
      const index = this.pendingRequests.findIndex((req) => req.id === requestId);
      
      if (index !== -1) {
        // Move the accepted request to acceptedRequests
        const acceptedRequest = this.pendingRequests[index];
        acceptedRequest.status = "accepted"; // Update status
        
        this.acceptedRequests.push(acceptedRequest); // Move to acceptedRequests
        this.pendingRequests.splice(index, 1); // Remove from pendingRequests
      }
    } else {
      console.error("Error:", result.message);
    }
  } catch (error) {
    console.error("Error accepting request:", error);
  }
},

      async rejectRequest(requestId) {
        try {
          await fetch(`/api/requests_sp/${requestId}`, { 
            method: "DELETE",
            headers: {
              "Authorization": `Bearer ${localStorage.getItem("serviceProfessionalToken")}`,
              "Content-Type": "application/json",
            }, 
            body: JSON.stringify({ action: "reject" })
           });
          this.fetchData(); // Refresh the data
        } catch (error) {
          console.error("Error rejecting request:", error);
        }
      },
        async closeRequest(requestId) {
    try {
      const response = await fetch(`/api/requests_sp/${requestId}`, {
        method: "PATCH",
        headers: {
          "Authorization": `Bearer ${localStorage.getItem("serviceProfessionalToken")}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ action: "close" }) // Send action
      });

      const result = await response.json();

      if (response.ok) {
        // Move the closed request from acceptedRequests to closedRequests
        const index = this.acceptedRequests.findIndex(req => req.id === requestId);
        if (index !== -1) {
          const closedRequest = this.acceptedRequests[index];
          closedRequest.status = "closed";
          closedRequest.date_closed = new Date().toISOString(); // Set closed date
          closedRequest.closed_by = result.closed_by; // Store who closed it

          this.closedRequests.push(closedRequest);
          this.acceptedRequests.splice(index, 1);
        }
      } else {
        console.error("Error closing request:", result.message);
      }
    } catch (error) {
      console.error("Error closing request:", error);
    }
  },
      async logout(){
        localStorage.removeItem("serviceProfessionalToken");
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
  