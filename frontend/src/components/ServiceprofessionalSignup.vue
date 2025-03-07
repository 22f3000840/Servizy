<template>
  <section class="vh-100 gradient-custom d-flex align-items-center">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-lg-8 col-md-10">
          <div class="card shadow-lg rounded-4 border-0">
            <div class="card-body p-5">
              <h2 class="text-center text-primary fw-bold mb-4">Service Professional Registration</h2>
              <form @submit.prevent="registerProfessional">
                
                <div class="mb-3">
                  <label class="form-label">Email</label>
                  <input type="email" v-model="email" class="form-control" required />
                </div>
                
                <div class="mb-3">
                  <label class="form-label">Username</label>
                  <input type="text" v-model="username" class="form-control" required />
                </div>
                
                <div class="mb-3">
                  <label class="form-label">Password</label>
                  <input type="password" v-model="password" class="form-control" required />
                </div>
                
                <div class="mb-3">
                  <label class="form-label">Select Service</label>
                  <select class="form-select" v-model="service" required>
                    <option v-for="service in services" :key="service.id" :value="service.service_name">
                      {{ service.service_name }}
                    </option>
                  </select>
                </div>
                
                <div class="mb-3">
                  <label class="form-label">Address</label>
                  <input type="text" v-model="address" class="form-control" required />
                </div>
                
                <div class="mb-3">
                  <label class="form-label">Pincode</label>
                  <input type="number" v-model="pincode" class="form-control" required />
                </div>
                
                <div class="text-center">
                  <button type="submit" class="btn btn-primary btn-lg w-100">Register</button>
                </div>
              </form>
              <router-link to="/" class="btn btn-outline-secondary w-100 mt-2">Home</router-link>
              
              <div v-if="errormessage" class="alert alert-danger mt-3 text-center">{{ errormessage }}</div>
              <div v-if="successmessage" class="alert alert-success mt-3 text-center">{{ successmessage }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  data() {
    return {
      services: [],
      email: "",
      username: "",
      password: "",
      service: "",
      address: "",
      pincode: "",
      errormessage: null,
      successmessage: null,
    };
  },
  mounted() {
    this.fetchServices();
  },
  methods: {
    async fetchServices() {
      try {
        const response = await fetch("/api/services");
        this.services = await response.json();
      } catch (error) {
        console.error("Error fetching services:", error);
      }
    },
    async registerProfessional() {
      this.errormessage = null;
      this.successmessage = null;
      const payload = {
        email: this.email,
        username: this.username,
        password: this.password,
        service: this.service,
        address: this.address,
        pincode: this.pincode,
        role: "service_professional",
      };
      try {
        const response = await fetch("/api/signupsp", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        });
        const result = await response.json();
        if (!response.ok) {
          this.errormessage = result.message || "An error occurred";
        } else {
          this.successmessage = result.message;
          setTimeout(() => this.$router.push("/service_professional-login"), 1500);
        }
      } catch (error) {
        this.errormessage = "Unable to connect to server";
      }
    },
  },
};
</script>

<style scoped>
.gradient-custom {
  background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
  min-height: 100vh;
  display: flex;
  align-items: center;
}
</style> 
