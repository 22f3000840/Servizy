<!--  <template> -->
    <!-- <div> -->
      <!-- Navbar -->
      <!-- <nav class="navbar navbar-expand-lg navbar-dark bg-danger"> -->
        <!-- <div class="container-fluid"> -->
          <!--  -->
          <template>
            <div class="admin-dashboard">
              <!-- Navbar -->
              <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-lg">
                <div class="container-fluid">
                  <a class="navbar-brand fw-bold text-uppercase" href="#">Admin Dashboard</a>
                  <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
                    aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                  </button>
                  <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav me-auto">
                      <li class="nav-item">
                        <router-link class="nav-link" to="/admin-dashboard">Home</router-link>
                      </li>
                      <li class="nav-item">
                        <router-link class="nav-link" to="/admin-dashboard/search">Search</router-link>
                      </li>
                      <li class="nav-item">
                        <a class="nav-link" @click="exportdata">Export CSV</a>
                      </li>
                      <li class="nav-item">
                        <a class="nav-link text-danger fw-bold" @click="logout">Logout</a>
                      </li>
                    </ul>
                    <ul class="navbar-nav ms-auto">
                      <li class="nav-item">
                        <span class="nav-link text-light fw-semibold">{{ adminName }}</span>
                      </li>
                    </ul>
                  </div>
                </div>
              </nav>
              <!-- Search Section -->
    <div class="container mt-5">
      <h2 class="section-title">Search Users</h2>
      <div class="input-group mb-3">
        <input
          type="text"
          class="form-control"
          placeholder="Search by username"
          v-model="searchQuery"
          @keyup.enter="searchUsers"
        />
        <button class="btn btn-primary" @click="searchUsers">Search</button>
      </div>

      <!-- Search Results -->
      <table v-if="searchResults.length" class="table table-hover table-striped shadow-sm">
        <thead class="table-dark">
          <tr>
            <th>Username</th>
            <th>Email</th>
            <th>Role</th>
            <th>Average Rating</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in searchResults" :key="user.id">
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.role }}</td>
            <td>{{ user.avg_rating}}</td>
            <td>{{ user.is_flagged ? "Blocked" : "Active" }}</td>
            <td>
              <button
                class="btn btn-sm"
                :class="user.is_flagged ? 'btn-success' : 'btn-danger'"
                @click="toggleBlockUser(user.id)"
              >
                {{ user.is_flagged ? "Unblock" : "Block" }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else class="text-center text-muted">No users found.</p>
    </div>
          
              <!-- Services Section -->
              <div class="container mt-5">
                <h2 class="section-title">Services</h2>
                <table v-if="services.length" class="table table-hover table-striped shadow-sm">
                  <thead class="table-dark">
                    <tr>
                      <th>Service Name</th>
                      <th>Description</th>
                      <th>Base Price</th>
                      <th>Time Required</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="service in services" :key="service.id">
                      <td>{{ service.service_name }}</td>
                      <td>{{ service.service_description }}</td>
                      <td>${{ service.base_price }}</td>
                      <td>{{ service.time_required }}</td>
                      <td>
                        <router-link :to="'/admin-dashboard/edit-service/' + service.id" class="btn btn-sm btn-primary me-2">Edit</router-link>
                        <button @click="deleteService(service.id)" class="btn btn-sm btn-danger">Delete</button>
                      </td>
                    </tr>
                  </tbody>
                </table>
                <p v-else class="text-center text-muted">No services found.</p>
                <router-link to="/admin-dashboard/create-service" class="btn btn-success mt-3">Create New Service</router-link>
              </div>
          
              <!-- Unapproved Service Professionals Section -->
              <div class="container mt-5">
                <h2 class="section-title">Unapproved Service Professionals</h2>
                <table v-if="unapprovedSP.length" class="table table-hover table-striped shadow-sm">
                  <thead class="table-dark">
                    <tr>
                      <th>Username</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="sp in unapprovedSP" :key="sp.id">
                      <td>{{ sp.username }}</td>
                      <td>
                        <button @click="approveSP(sp.id)" class="btn btn-sm btn-success me-2">Approve</button>
                        <button @click="rejectSP(sp.id)" class="btn btn-sm btn-danger">Reject</button>
                      </td>
                    </tr>
                  </tbody>
                </table>
                <p v-else class="text-center text-muted">No unapproved service professionals found.</p>
              </div>
          
              <!-- Requests Section -->
              <div class="container mt-5 mb-5">
                <h2 class="section-title">Requests</h2>
                <table v-if="requests.length" class="table table-hover table-striped shadow-sm">
                  <thead class="table-dark">
                    <tr>
                      <th>ID</th>
                      <th>Service Professional</th>
                      <th>Requested Date</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="request in requests" :key="request.id">
                      <td>{{ request.id }}</td>
                      <td>
                        <!-- <router-link :to="'/admin_dashboard/view_sp/' + request.service_professional.id"> -->
                          {{ request.service_professional.user_name }}
                        <!-- </router-link> -->
                      </td>
                      <td>{{ request.date_created }}</td>
                      <td>{{ request.status }}</td>
                    </tr>
                  </tbody>
                </table>
                <p v-else class="text-center text-muted">No requests found.</p>
              </div>
            </div>
          </template>
          
          <script>
          export default {
            data() {
              return {
                searchQuery: "",
                searchResults: [],
                services: [],
                unapprovedSP: [],
                requests: [],
                adminName: "Admin", // Dynamically set if needed
              };
            },
            mounted() {
              this.fetchServices();
              this.fetchUnapprovedSP();
              this.fetchRequests();
            },
            methods: {
              async searchUsers() {
      try {
        const response = await fetch(`/api/admin_dashboard/search?search_type=user&search_query=${this.searchQuery}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("adminToken")}`,
          },
        });
        const data = await response.json();
        this.searchResults = data.users || [];
      } catch (error) {
        console.error("Error searching users:", error);
      }
    },
    async toggleBlockUser(userId) {
  try {
    const response = await fetch(`/api/admin_dashboard/search/${userId}`, {
      method: "PATCH",
      headers: {
        Authorization: `Bearer ${localStorage.getItem("adminToken")}`,
      },
    });
    const data = await response.json();
    if (response.ok) {
      alert(data.message);

      // Update the user's status in the searchResults array
      this.searchResults = this.searchResults.map(user => {
        if (user.id === userId) {
          return { ...user, is_flagged: !user.is_flagged }; // Toggle the is_flagged status
        }
        return user;
      });
    } else {
      alert("Error updating user status");
    }
  } catch (error) {
    console.error("Error toggling block status:", error);
  }
},
              async fetchServices() {
                try {
                  const response = await fetch("/api/services");
                  this.services = await response.json();
                } catch (error) {
                  console.error("Error fetching services:", error);
                }
              },
              async fetchUnapprovedSP() {
                try {
                  const response = await fetch("/api/sp", {
                    headers: {
                      Authorization: `Bearer ${localStorage.getItem("adminToken")}`,
                    },
                  });
                  this.unapprovedSP = await response.json();
                } catch (error) {
                  console.error("Error fetching unapproved service professionals:", error);
                }
              },
              async fetchRequests() {
                try {
                  const response = await fetch("/api/requests", {
                    headers: {
                      Authorization: `Bearer ${localStorage.getItem("adminToken")}`,
                    },
                  });
          
                  if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
          
                  const data = await response.json();
                  this.requests = data.requests || [];
                } catch (error) {
                  console.error("Error fetching requests:", error);
                }
              },
              async deleteService(serviceId) {
                if (!confirm("Are you sure you want to delete this service?")) return;
                try {
                  const response = await fetch(`/api/services/${serviceId}`, {
                    method: "DELETE",
                    headers: {
                      Authorization: `Bearer ${localStorage.getItem("adminToken")}`,
                    },
                  });
          
                  if (response.ok) {
                    alert("Service deleted successfully!");
                    this.fetchServices();
                  } else {
                    alert("Error deleting service");
                  }
                } catch (error) {
                  console.error("Error deleting service:", error);
                }
              },
              async approveSP(spId) {
                try {
                  await fetch(`/api/sp/${spId}`, {
                    method: "PATCH",
                    headers: {
                      Authorization: `Bearer ${localStorage.getItem("adminToken")}`,
                    },
                  });
                  alert("Service professional approved!");
                  this.fetchUnapprovedSP();
                } catch (error) {
                  console.error("Error approving SP:", error);
                }
              },
              async rejectSP(spId) {
                try {
                  await fetch(`/api/sp/${spId}`, {
                    method: "DELETE",
                    headers: {
                      Authorization: `Bearer ${localStorage.getItem("adminToken")}`,
                    },
                  });
                  alert("Service professional rejected.");
                  this.fetchUnapprovedSP();
                } catch (error) {
                  console.error("Error rejecting SP:", error);
                }
              },
              logout() {
                localStorage.removeItem("adminToken");
                this.$router.push("/");
              },
              async exportdata() {
        try {
            const sp_id = prompt("Enter Service Professional ID to export data for:");
            if (!sp_id) return;

            const response = await fetch(`/api/admin_dashboard/export_data/${sp_id}`, {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${localStorage.getItem("adminToken")}`,
                    "Content-Type": "application/json"
                }
            });

            if (response.ok) {
                const result = await response.json();
                alert(result.message);
            } else {
                const errorData = await response.json();
                alert(`Error exporting data: ${errorData.error || "Unknown error"}`);
            }
        } catch (error) {
            console.error("Error exporting data:", error);
            alert("An error occurred while exporting data.");
        }
    },
    },
  };
          </script>
          
          <style scoped>
          .section-title {
            text-align: center;
            font-weight: bold;
            margin-bottom: 20px;
          }
          </style>
          
  