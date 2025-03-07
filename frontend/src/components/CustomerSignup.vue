<!-- <template>
    <section class="vh gradient-custom">
      <div class="container h-100">
        <div class="row d-flex justify-content-center align-items-center h-100">
          <div class="col-xl-9">
            <h1 class="text-white mb-4">Customer Registration</h1>
            <form @submit.prevent="registerCustomer">
              <div class="card" style="border-radius: 15px;">
                <div class="card-body">
                  <div class="row align-items-center py-3">
                    <div class="col-md-3 ps-5">
                      <h6 class="mb-0">Email</h6>
                    </div>
                    <div class="col-md-9 pe-5">
                      <input type="text" v-model="email" class="form-control form-control-lg" required />
                    </div>
                  </div>
                  <div class="row align-items-center pt-4 pb-3">
                    <div class="col-md-3 ps-5">
                      <h6 class="mb-0">Username</h6>
                    </div>
                    <div class="col-md-9 pe-5">
                      <input type="text" v-model="username" class="form-control form-control-lg" required />
                    </div>
                  </div>
  
                  <div class="row align-items-center py-3">
                    <div class="col-md-3 ps-5">
                      <h6 class="mb-0">Password</h6>
                    </div>
                    <div class="col-md-9 pe-5">
                      <input type="password" v-model="password" class="form-control form-control-lg" required />
                    </div>
                  </div>
  
                  <hr class="mx-n3">
                  <div class="row align-items-center py-3">
                    <div class="col-md-3 ps-5">
                      <h6 class="mb-0">Address</h6>
                    </div>
                    <div class="col-md-9 pe-5">
                      <input type="text" v-model="address" class="form-control form-control-lg" required />
                    </div>
                  </div>
  
                  <hr class="mx-n3">
                  <div class="row align-items-center py-3">
                    <div class="col-md-3 ps-5">
                      <h6 class="mb-0">Pincode</h6>
                    </div>
                    <div class="col-md-9 pe-5">
                      <input type="number" v-model="pincode" class="form-control form-control-lg" required />
                    </div>
                  </div>
  
                  <hr class="mx-n3">
                  <div class="text-center text-lg-start mt-4 pt-2">
                    <button type="submit" class="btn btn-primary btn-lg">
                      Register
                    </button>
                  </div>
                </div>
              </div>
            </form>
  
            <div v-if="errormessage" class="alert alert-danger mt-3">  {{ errormessage }} </div>
            <div v-if="successmessage" class="alert alert-success mt-3">  {{ successmessage }} </div>
            
            
          </div>
        </div>
      </div>
    </section>
  </template>

<script>
export default {
  data() {
    return {
      email: "",
      username: "",
      password: "",
      address: "",
      pincode: "",
      errormessage: null,
      successmessage: null,
    };
  },
  methods: {
    async registerCustomer() {
      this.errormessage = null;
      this.successmessage = null;
      const payload = {
        email: this.email,
        username: this.username,
        password: this.password,
        address: this.address,
        pincode: this.pincode,
        role: "customer",
      };
      try {
        const response = await fetch("/api/signupcu", {
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
          alert(result.message);
          this.$router.push("/customer-login");
        }
        
      } catch (error) {
        this.errormessage = "Unable to connect server";
      }
    },
  },
};
</script> -->


<template>
  <section class="vh-100 d-flex align-items-center justify-content-center bg-light">
      <div class="container">
          <div class="row justify-content-center">
              <div class="col-md-8">
                  <div class="card shadow-lg p-4 rounded border-0">
                      <div class="card-body">
                          <h2 class="text-center text-primary mb-4">Customer Registration</h2>
                          <form @submit.prevent="registerCustomer">
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
                                  <label class="form-label">Address</label>
                                  <input type="text" v-model="address" class="form-control" required />
                              </div>
                              <div class="mb-3">
                                  <label class="form-label">Pincode</label>
                                  <input type="number" v-model="pincode" class="form-control" required />
                              </div>
                              <div class="d-grid">
                                  <button type="submit" class="btn btn-primary btn-lg">Register</button>
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
          email: "",
          username: "",
          password: "",
          address: "",
          pincode: "",
          errormessage: null,
          successmessage: null,
      };
  },
  methods: {
      async registerCustomer() {
          this.errormessage = null;
          this.successmessage = null;
          const payload = {
              email: this.email,
              username: this.username,
              password: this.password,
              address: this.address,
              pincode: this.pincode,
              role: "customer",
          };
          try {
              const response = await fetch("/api/signupcu", {
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
                  alert(result.message);
                  this.$router.push("/customer-login");
              }
          } catch (error) {
              this.errormessage = "Unable to connect to the server";
          }
      },
  },
};
</script>

<style>
body {
  background: linear-gradient(135deg, #667eea, #764ba2);
}
</style>


