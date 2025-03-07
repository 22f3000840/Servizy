<template>
    <div>
      <!-- Navbar -->
      <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container-fluid">
          <router-link class="navbar-brand" to="/customer_dashboard">Customer Dashboard</router-link>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
              <li class="nav-item"><router-link class="nav-link" to="/customer_dashboard">Home</router-link></li>
              <li class="nav-item"><router-link class="nav-link" to="/customer_dashboard/search">Search</router-link></li>
              <li class="nav-item"><router-link class="nav-link" to="/summary">Summary</router-link></li>
              <li class="nav-item"><router-link class="nav-link" to="/logout">Logout</router-link></li>
            </ul>
          </div>
        </div>
      </nav>
  
      <!-- Rating Form -->
      <!-- <div class="container mt-4">
    <h2>Rate and Review Service</h2>
    <p>Rate and review the service provided.</p>

    <Rating Section -->
      <div class="container mt-4">
    <h2>Review & Rate Service</h2>
    <p>Service Request ID: {{ requestId }}</p>

    <form @submit.prevent="submitReview">
      <div>
        <label>Rating:</label>
        <select v-model="rating" required>
          <option value="5">⭐⭐⭐⭐⭐</option>
          <option value="4">⭐⭐⭐⭐</option>
          <option value="3">⭐⭐⭐</option>
          <option value="2">⭐⭐</option>
          <option value="1">⭐</option>
        </select>
      </div>
      <div>
        <label>Review:</label>
        <textarea v-model="review" required></textarea>
      </div>
      <button type="submit" class="btn btn-primary">Submit Review</button>
    </form>

    <p v-if="successMessage" class="text-success">{{ successMessage }}</p>
  </div>
  </div>
  </template>
  
  <script>
export default {
  data() {
    return {
      requestId: this.$route.params.requestId,
      rating: 0,
      review: "",
      successMessage: "",
    };
  },
  methods: {
      async submitReview() {
    try {
      if (!this.rating || !this.review.trim()) {
        alert("Please provide a rating and review.");
        return;
      }

      // Ensure rating is between 1 and 5
      const ratingInt = parseInt(this.rating, 10);
      if (isNaN(ratingInt) || ratingInt < 1 || ratingInt > 5) {
        alert("Invalid rating: Please provide a number between 1 and 5.");
        return;
      }

      // Prepare the request payload
      const payload = {
        rating: ratingInt,
        review: this.review.trim(),
      };

      // Send POST request to close request and submit review
      const response = await fetch(`/api/customer_dashboard/close_request/${this.requestId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + localStorage.getItem("customerToken"),
        },
        body: JSON.stringify(payload),
      });

      const responseData = await response.json();

      if (response.ok) {
        alert("Service request closed successfully!");
        this.$router.push("/customer-dashboard"); // Redirect back to dashboard
      } else {
        alert(`Error: ${responseData.message}`);
      }
    } catch (error) {
      console.error("Error submitting review:", error);
      alert("An error occurred while submitting your review. Please try again.");
    }
  },

  },
};
</script>

<style>
.fas.fa-star {
  color: gold;
  cursor: pointer;
}
</style>