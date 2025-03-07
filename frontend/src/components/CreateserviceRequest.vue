<template>
    <div class="container mt-5">
      <h2>Create Service Request in {{ serviceName }}</h2>
      
      <form @submit.prevent="submitRequest">
        <div class="form-group">
          <label for="service_name">Service Name:</label>
          <input type="text" class="form-control" id="service_name" v-model="serviceName" readonly>
        </div>
  
        <div class="form-group">
          <label for="service_professional">Service Professional:</label>
          <select class="form-control" id="service_professional" v-model="selectedProfessional">
            <option v-for="sp in serviceProfessionals" :key="sp.user_name" :value="sp.user_name">
              {{ sp.user_name }}
            </option>
          </select>
        </div>
  
        <div class="form-group">
          <label for="description">Description:</label>
          <textarea class="form-control" id="description" v-model="description" rows="5"></textarea>
        </div>
  
        <button type="submit" class="btn btn-primary">Create Request</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        serviceId: null,
        serviceName: '',
        serviceProfessionals: [],
        selectedProfessional: '',
        description: ''
      };
    },
    mounted() {
      this.fetchServiceDetails();
    },
    methods: {
      async fetchServiceDetails() {
        try {
          const response = await fetch(`/api/service_details/${this.$route.params.serviceId}`, {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              "Authorization": "Bearer " + localStorage.getItem("customerToken")
            }
          });
          if (!response.ok) {
            throw new Error("Failed to fetch service details");
          }
          const data = await response.json();
  
          this.serviceId = data.service.id;
          this.serviceName = data.service.service_name;
          this.serviceProfessionals = data.service_professionals;
        } catch (error) {
          console.error("Error fetching service details:", error);
        }
      },
      async submitRequest() {
        try {
          console.log("Selected Professional:", this.selectedProfessional);
          console.log("Description:", this.description);
          const response = await fetch(`/api/customer_dashboard/create_service_request/${this.$route.params.serviceId}`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authorization": "Bearer " + localStorage.getItem("customerToken")
            },
            body: JSON.stringify({
              service_professional: this.selectedProfessional,
              description: this.description
            })
          });
  
          if (!response.ok) {
            throw new Error("Failed to create service request");
          }
  
          alert("✅ Service request created successfully!");
          this.$router.push("/customer-dashboard");
        } catch (error) {
          console.error("Error creating request:", error);
          alert("❌ Failed to create service request!");
        }
      }
    }
  };
  </script>
  
  <style>
  /* Add custom styles if needed */
  </style>
  