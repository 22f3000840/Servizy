<!-- <template>
    <div class="mt-5">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">Service Professional Login
                        <div class="card-body">
                            <form @submit.prevent="loginServiceProfessional">
                                <div class="form-group">
                                    <label for="email">Email address</label>
                                    <input type="email" class="form-control" id="email" v-model="email" required>
                                </div>
                                <div class="form-group">
                                    <label for="password">Password</label>
                                    <input type="password" class="form-control" id="password" v-model="password" required>
                    
                                </div>
                                <div v-if="errorMessage" class="text-danger">{{ errorMessage }} </div>
                                
                                
                                <button type="submit" class="btn btn-primary">Login</button>
                                <router-link to="/service_professional-signup" class="btn btn-secondary mx-3">Signup</router-link>
            
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
export default {
    data() {
        return {
            email: '',
            password: '',
            errorMessage: ''
        }
    },
    methods: {
        async loginServiceProfessional() {
            this.errorMessage=null;
            const payload={email: this.email, password: this.password};
            try {
                const response=await fetch("/api/login", {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload),
                });
                const result=await response.json();
                if(!response.ok){
                    this.errorMessage=result.message || "An error occurred";
                }else{
                    if (result.user_role=="service_professional") {
                        alert("Logged in successfully");
                        localStorage.setItem("serviceProfessionalToken", result.token);
                        this.$router.push("/service-professional-dashboard");
                    }else{
                        alert("not authorized to access this page");
                    }
                   
                }
            }
            catch (error) {
                this.errorMessage="Unable to connect server";
            }
        },
    },
};
</script> -->



<template>
    <section class="d-flex justify-content-center align-items-center min-vh-100 bg-gradient">
      <div class="card shadow-lg p-4 rounded-4" style="max-width: 400px; width: 100%;">
        <div class="card-body">
          <h3 class="text-center mb-4">Service Professional Login</h3>
          <form @submit.prevent="loginServiceProfessional">
            <div class="mb-3">
              <label for="email" class="form-label">Email Address</label>
              <input type="email" class="form-control" id="email" v-model="email" required>
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">Password</label>
              <input type="password" class="form-control" id="password" v-model="password" required>
            </div>
            <div v-if="errorMessage" class="alert alert-danger p-2 text-center">{{ errorMessage }}</div>
            <button type="submit" class="btn btn-primary w-100">Login</button>
            <router-link to="/service_professional-signup" class="btn btn-outline-secondary w-100 mt-2">Signup</router-link>
          </form>
          <router-link to="/" class="btn btn-outline-secondary w-100 mt-2">Home</router-link>
        </div>
      </div>
    </section>
  </template>
  
  <script>
  export default {
    data() {
      return {
        email: '',
        password: '',
        errorMessage: ''
      };
    },
    methods: {
      async loginServiceProfessional() {
        this.errorMessage = null;
        const payload = { email: this.email, password: this.password };
        try {
          const response = await fetch("/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
          });
          const result = await response.json();
          if (!response.ok) {
            this.errorMessage = result.message || "An error occurred";
          } else {
            if (result.user_role === "service_professional") {
              alert("Logged in successfully");
              localStorage.setItem("serviceProfessionalToken", result.token);
              this.$router.push("/service-professional-dashboard");
            } else {
              alert("Not authorized to access this page");
            }
          }
        } catch (error) {
          this.errorMessage = "Unable to connect to server";
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .bg-gradient {
    background: linear-gradient(135deg, #6a11cb, #2575fc);
    height: 100vh;
  }
  .card {
    background: #ffffff;
    border-radius: 10px;
  }
  </style>
  



