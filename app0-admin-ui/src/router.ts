import { createRouter as createClientRouter, createWebHistory } from 'vue-router'

/**
 * routes are generated using vite-plugin-pages
 * each .vue files located in the ./src/pages are registered as a route
 * @see https://github.com/hannoeru/vite-plugin-pages
 */
// import routes from 'pages-generated'

/**
 * Here is how a simple route is generated:
 * import { RouteRecordRaw } from 'vue-router'
 *
 * const routes: RouteRecordRaw = [{
 *    component: () => import('/src/pages/wizard-1.vue'),
 *    name: 'wizard-v1',
 *    path: '/wizard-v1',
 *    props: true,
 *    meta: {
 *      requiresAuth: true
 *    },
 * }]
 *
 * Here is how nested routes are generated:
 * import { RouteRecordRaw } from 'vue-router'
 *
 * const routes: RouteRecordRaw = [{
 *    component: () => import('/src/pages/auth.vue'),
 *    path: '/auth',
 *    props: true,
 *    children: [
 *      {
 *        component: () => import('/src/pages/auth/login-1.vue'),
 *        name: 'auth-login-1',
 *        path: 'login-1',
 *        props: true
 *      },
 *    ],
 * }]
 *
 * Uncomment the line below to view the generated routes
 */
// console.log(routes)
import { RouteRecordRaw } from 'vue-router'
const routes: RouteRecordRaw[] = [
  {
    component: () => import('/src/pages/index.vue'),
    name: 'index',
    path: '/',
    props: true,
    meta: { requiresAuth: true },
    // beforeEnter: authGuard,
  },
  {
    component: () => import('/src/pages/home.vue'),
    name: 'home',
    path: '/home',
    props: true,
    meta: { requiresAuth: true },
    // beforeEnter: authGuard,
  },
  {
    component: () => import('/src/pages/users.vue'),
    name: 'users',
    path: '/users',
    props: true,
    meta: { requiresAuth: true },
    // beforeEnter: authGuard,
  },
  {
    component: () => import('/src/pages/user-edit.vue'),
    name: 'user-edit',
    path: '/user/:objId',
    props: true,
    meta: { requiresAuth: true },
    // beforeEnter: authGuard,
  },
  {
    component: () => import('/src/pages/tmails.vue'),
    name: 'tmails',
    path: '/tmails',
    props: true,
    meta: { requiresAuth: true },
    // beforeEnter: authGuard,
  },
  {
    component: () => import('/src/pages/tmail-edit.vue'),
    name: 'tmail-edit',
    path: '/tmail/:objId',
    props: true,
    meta: { requiresAuth: true },
    // beforeEnter: authGuard,
  },
  {
    component: () => import('/src/pages/plans.vue'),
    name: 'plans',
    path: '/plans',
    props: true,
    meta: { requiresAuth: true },
    // beforeEnter: authGuard,
  },
  {
    component: () => import('/src/pages/plan-edit.vue'),
    name: 'plan-edit',
    path: '/plan/:objId',
    props: true,
    meta: { requiresAuth: true },
    // beforeEnter: authGuard,
  },
  {
    component: () => import('/src/pages/registration-wizard.vue'),
    name: 'registration-wizard',
    path: '/registration/w',
    props: true,
  },
  {
    component: () => import('/src/pages/registrations.vue'),
    name: 'registrations',
    path: '/registrations',
    props: true,
    meta: { requiresAuth: true },
    // beforeEnter: authGuard,
  },
  {
    component: () => import('/src/pages/registration-edit.vue'),
    name: 'registration-edit',
    path: '/registration/:objId',
    props: true,
    meta: { requiresAuth: true },
    // beforeEnter: authGuard,
  },
  {
    component: () => import('/src/pages/profile.vue'),
    name: 'profile',
    path: '/profile',
    props: true,
    meta: { requiresAuth: true },
    // beforeEnter: authGuard,
  },
  {
    component: () => import('/src/pages/profile-notifications.vue'),
    name: 'profile-notifications',
    path: '/profile-notifications',
    props: true,
    meta: { requiresAuth: true },
    // beforeEnter: authGuard,
  },
  {
    component: () => import('/src/pages/apps.vue'),
    name: 'apps',
    path: '/apps',
    props: true,
    meta: { requiresAuth: true },
    // beforeEnter: authGuard,
  },
  {
    component: () => import('/src/pages/app-edit.vue'),
    name: 'app-edit',
    path: '/app/:objId',
    props: true,
    meta: { requiresAuth: true },
    // beforeEnter: authGuard,
  },
  {
    component: () => import('/src/pages/roles.vue'),
    name: 'roles',
    path: '/roles',
    props: true,
    meta: { requiresAuth: true },
    // beforeEnter: authGuard,
  },
  {
    component: () => import('/src/pages/role-edit.vue'),
    name: 'role-edit',
    path: '/role/:objId',
    props: true,
    meta: { requiresAuth: true },
    // beforeEnter: authGuard,
  },
  {
    component: () => import('/src/pages/error/error-page-4.vue'),
    name: 'error-page-4',
    path: '/error-page-4',
    props: true,
  },
  {
    component: () => import('/src/pages/error/error-page-5.vue'),
    name: 'error-page-5',
    path: '/error-page-5',
    props: true,
  },
  {
    component: () => import('/src/pages/auth/login.vue'),
    name: 'login',
    path: '/login',
    props: true,
  },
  {
    component: () => import('/src/pages/auth/logout.vue'),
    name: 'logout',
    path: '/logout',
    props: true,
  },
  {
    component: () => import('/src/pages/auth/reset.vue'),
    name: 'reset',
    path: '/reset/:token',
    props: true,
  },
  {
    component: () => import('/src/pages/auth/first-set.vue'),
    name: 'first-set',
    path: '/fset/:token',
    props: true,
  },
  {
    component: () => import('/src/pages/[...all].vue'),
    name: 'all',
    path: '/:all(.*)',
    props: true,
  },
]

export function createRouter() {
  const router = createClientRouter({
    history: createWebHistory('admin'),
    routes,
  })

  return router
}
