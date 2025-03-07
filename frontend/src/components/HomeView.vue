
<!-- <template>
    <div class="d-flex align items-center vh-100">
        <div class="w-50 mx-auto">
            <div class="card w-50">
                <div class="card-header text-center">Welcome to Household Servicing App</div>
                <div class="card-body d-flex justify-content-around">
                <h5 class="card-title">Select your role:</h5>
                <blockquote class="blockquote mb-0">
                    <router-link to="/admin-login" class="btn btn-primary mx-3">Admin</router-link>
                    <router-link to="/service_professional-login" class="btn btn-secondary mx-3">Service_professional</router-link>
                    <router-link to="/customer-login" class="btn btn-danger mx-3">Customer</router-link>
                </blockquote>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  name: "HomeView",
};
</script> -->
<template>
    <div class="d-flex align-items-center justify-content-center vh-100 bg-light">
      <div class="card shadow-lg p-4 rounded-lg text-center" style="max-width: 450px;">
        <div class="card-header bg-primary text-white fw-bold fs-4">
          Welcome to Household Servicing App
        </div>
        <div class="card-body">
          <h5 class="card-title mb-4">Select Your Role</h5>
          <div class="d-flex flex-column gap-3">
            <router-link to="/admin-login" class="btn btn-primary btn-lg fw-semibold">
              Admin
            </router-link>
            <router-link to="/service_professional-login" class="btn btn-secondary btn-lg fw-semibold">
              Service Professional
            </router-link>
            <router-link to="/customer-login" class="btn btn-danger btn-lg fw-semibold">
              Customer
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "HomeView",
  };
  </script> 
  
