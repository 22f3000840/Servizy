<!-- <template>
    <div class="mt-5">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">Customer Login
                        <div class="card-body">
                            <form @submit.prevent="loginUser">
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
                                <router-link to="/customer-signup" class="btn btn-secondary mx-3">Signup</router-link>
            
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
        async loginUser() {
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
                    if (result.user_role=="customer") {
                        alert("Logged in successfully");
                        localStorage.setItem("customerToken", result.token);
                        this.$router.push("/customer-dashboard");
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
    <section class="vh-100 d-flex align-items-center justify-content-center gradient-custom">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-md-6">
                    <div class="card shadow-lg border-0 rounded-3">
                        <div class="card-body p-5">
                            <h2 class="text-center text-primary mb-4">Customer Login</h2>
                            <form @submit.prevent="loginUser">
                                <div class="mb-3">
                                    <label for="email" class="form-label">Email address</label>
                                    <input type="email" class="form-control form-control-lg" id="email" v-model="email" required>
                                </div>
                                <div class="mb-3">
                                    <label for="password" class="form-label">Password</label>
                                    <input type="password" class="form-control form-control-lg" id="password" v-model="password" required>
                                </div>
                                <div v-if="errorMessage" class="alert alert-danger text-center">{{ errorMessage }}</div>
                                <div class="d-grid">
                                    <button type="submit" class="btn btn-primary btn-lg">Login</button>
                                </div>
                                <div class="text-center mt-3">
                                    <router-link to="/customer-signup" class="btn btn-link text-decoration-none">Don't have an account? Sign Up</router-link>
                                </div>
                            </form>
                            <router-link to="/" class="btn btn-outline-secondary w-100 mt-2">Home</router-link>
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
            email: '',
            password: '',
            errorMessage: ''
        }
    },
    methods: {
        async loginUser() {
            this.errorMessage = null;
            const payload = { email: this.email, password: this.password };
            try {
                const response = await fetch("/api/login", {
                    method: "POST",
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload),
                });
                const result = await response.json();
                if (!response.ok) {
                    this.errorMessage = result.message || "An error occurred";
                } else {
                    if (result.user_role === "customer") {
                        alert("Logged in successfully");
                        localStorage.setItem("customerToken", result.token);
                        this.$router.push("/customer-dashboard");
                    } else {
                        this.errorMessage = "Not authorized to access this page";
                    }
                }
            } catch (error) {
                this.errorMessage = "Unable to connect to server";
            }
        },
    },
};
</script>

<style>
.gradient-custom {
    background: linear-gradient(to right, #6a11cb, #2575fc);
}
.card {
    border-radius: 15px;
}
</style>

