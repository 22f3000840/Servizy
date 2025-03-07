<!-- <template>
    <div class="mt-5">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">Admin Login
                        <div class="card-body">
                            <form @submit.prevent="loginAdmin">
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
        async loginAdmin() {
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
                    if (result.user_role=="admin") {
                        alert("Logged in successfully");
                        localStorage.setItem("adminToken", result.token);
                        this.$router.push("/admin-dashboard");
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
    <div class="login-container">
      <div class="overlay"></div>
      <div class="d-flex align-items-center justify-content-center vh-100">
        <div class="card shadow-lg p-4 rounded-lg">
          <div class="card-header bg-primary text-white text-center fw-bold fs-4">
            Admin Login
          </div>
          <div class="card-body">
            <form @submit.prevent="loginAdmin">
              <div class="mb-3">
                <label for="email" class="form-label fw-semibold">Email Address</label>
                <input type="email" class="form-control rounded-pill" id="email" v-model="email" required />
              </div>
              <div class="mb-3">
                <label for="password" class="form-label fw-semibold">Password</label>
                <input type="password" class="form-control rounded-pill" id="password" v-model="password" required />
              </div>
              <div v-if="errorMessage" class="alert alert-danger text-center py-2">
                {{ errorMessage }}
              </div>
              <button type="submit" class="btn btn-primary w-100 rounded-pill fw-bold">
                Login
              </button>
            </form>
            <router-link to="/" class="btn btn-outline-secondary w-100 mt-2">Home</router-link>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        email: "",
        password: "",
        errorMessage: "",
      };
    },
    methods: {
      async loginAdmin() {
        this.errorMessage = null;
        const payload = { email: this.email, password: this.password };
        try {
          const response = await fetch("/api/login", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
          });
          const result = await response.json();
          if (!response.ok) {
            this.errorMessage = result.message || "An error occurred";
          } else {
            if (result.user_role === "admin") {
              alert("Logged in successfully");
              localStorage.setItem("adminToken", result.token);
              this.$router.push("/admin-dashboard");
            } else {
              this.errorMessage = "Not authorized to access this page.";
            }
          }
        } catch (error) {
          this.errorMessage = "Unable to connect to the server.";
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* Background Styling */
  .login-container {
    position: relative;
    height: 100vh;
    background: url('https://source.unsplash.com/1600x900/?technology,admin') no-repeat center center;
    background-size: cover;
  }
  
  /* Overlay Effect */
  .overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5); /* Dark overlay */
  }
  
  /* Centered Card */
  .card {
    width: 400px;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 12px;
    position: relative;
    z-index: 1;
  }
  
  /* Input Styling */
  .form-control {
    border: 2px solid #ccc;
    transition: border-color 0.3s ease-in-out;
  }
  
  .form-control:focus {
    border-color: #007bff;
    box-shadow: 0 0 8px rgba(0, 123, 255, 0.5);
  }
  
  /* Button Styling */
  .btn {
    transition: all 0.3s ease-in-out;
  }
  
  .btn:hover {
    transform: scale(1.05);
  }
  </style>
  