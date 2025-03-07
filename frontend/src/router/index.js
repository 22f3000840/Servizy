import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/components/HomeView.vue';
import AdminLogin from '@/components/AdminLogin.vue';
import CustomerLogin from '@/components/CustomerLogin.vue';
import ServiceprofessionalLogin from '@/components/ServiceprofessionalLogin.vue';
import ServiceprofessionalSignup from '@/components/ServiceprofessionalSignup.vue';
import CustomerSignup from '@/components/CustomerSignup.vue';
import AdminDashboard from '@/components/AdminDashboard.vue';
import CreateService from '@/components/CreateService.vue';
import EditService from '@/components/EditService.vue';
import AdminSearch from '@/components/AdminSearch.vue';
import CustomerDashboard from '@/components/CustomerDashboard.vue';
import CreateserviceRequest from '@/components/CreateserviceRequest.vue';
import EditserviceRequest from '@/components/EditserviceRequest.vue';
import CustomerSearch from '@/components/CustomerSearch.vue';
import ServiceprofessionalDashboard from '@/components/ServiceprofessionalDashboard.vue';
import ReviewRating from '@/components/ReviewRating.vue';
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/admin-login',
      name: 'admin-login',
      component: AdminLogin,
    },
    {
      path: '/customer-login',
      name: 'customer-login',
      component: CustomerLogin,
    },
    {
      path: '/service_professional-login',
      name: 'serviceprofessional-login',
      component: ServiceprofessionalLogin,
    },
    {
      path: '/service_professional-signup',
      name: 'serviceprofessional-signup',
      component: ServiceprofessionalSignup,
    },
    {
      path: '/customer-signup',
      name: 'customer-signup',
      component: CustomerSignup,
    },
    {
      path: '/admin-dashboard',
      name: 'admin-dashboard',
      component: AdminDashboard,
    },
    {
      path: '/admin-dashboard/create-service',
      name: 'create-service',
      component: CreateService,
    },
    {
      path: '/admin-dashboard/edit-service/:id',
      name: 'edit-service',
      component: EditService,
    },
    {
      path: '/admin-dashboard/search',
      name: 'admin-search',
      component: AdminSearch,
    },
    {
      path: '/admin-dashboard/search/:userId',
      name: 'admin-search-id',
      component: AdminSearch,
    },
    {
      path: '/customer-dashboard',
      name: 'customer-dashboard',
      component: CustomerDashboard,
    },
    {
      path: '/customer-dashboard/create-service-request/:serviceId',
      name: 'create-service-request',
      component: CreateserviceRequest,
    },
    {
      path: '/customer-dashboard/edit-service-request/:requestId',
      name: 'edit-service-request',
      component: EditserviceRequest,
    },
    {
      path: '/customer-dashboard/review-rating/:requestId',
      name: 'review-rating',
      component: ReviewRating,
    },
    {
      path: '/customer-dashboard/search',
      name: 'customer-search',
      component: CustomerSearch,
    },
    {
      path: '/service-professional-dashboard',
      name: 'serviceprofessional-dashboard',
      component: ServiceprofessionalDashboard,
    },


    
  ],
})

export default router
