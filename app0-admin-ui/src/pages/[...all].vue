<script setup lang="ts">
/**
 * This is a Vue Component that will be
 * automatically mapped to a catch allpath on vue-router (404).
 *
 * You will be able to access this page  at http://localhost:3000/non-existing-page
 *
 * Read more about routing:
 * @see /vite.config.ts
 * @see /src/router.ts
 */

import { useHead } from '@vueuse/head'
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
// const { t } = useI18n()

onMounted(() => {
  /**
   * replacing path with a leading /404 allow us to detect this
   * on nginx to return a real 404 status code
   *
   * @see /src/nginx/vuejs.conf
   */
  if (!route.path.startsWith('/404')) {
    window.location.href = `/admin/404${route.fullPath}`
  }
})

useHead({
  title: 'Page not found - Platform',
  meta: [
    {
      name: 'robots',
      content: 'noindex',
    },
  ],
})
</script>

<template>
  <MinimalLayout>
    <div class="error-container">
      <div class="error-wrapper">
        <div class="error-inner has-text-centered">
          <div class="bg-number">404</div>
          <SVGErrorPlaceholder />
          <h3>We couldn't find that page</h3>
          <p>
            Looks like we couldn't find that page. Please try again or contact an administrator if the problem persists.
          </p>
          <div class="button-wrap">
            <VButton color="primary" elevated :to="{ name: 'index' }"> Take me Back </VButton>
          </div>
        </div>
      </div>
    </div>
  </MinimalLayout>
</template>

<style lang="scss">
.error-container {
  .error-wrapper {
    max-width: 840px;
    margin: 0 auto;
    padding-top: 40px;

    .error-inner {
      position: relative;
      max-width: 540px;
      margin: 0 auto;

      .bg-number {
        font-family: var(--font);
        position: absolute;
        top: -58px;
        left: -50px;
        right: 0;
        margin: 0 auto;
        font-size: 28rem;
        font-weight: 600;
        opacity: 0.15;
        z-index: 0;
      }

      img,
      svg,
      h3,
      p,
      .button-wrap {
        position: relative;
        z-index: 1;
      }

      img,
      svg {
        display: block;
        max-width: 100%;
        margin: 0 auto;
      }

      h3 {
        font-size: 1.5rem;
        font-family: var(--font-alt);
        color: var(--dark-text);
        font-weight: 600;
        margin-top: 10px;
      }

      p {
        font-family: var(--font);
        font-size: 1.1rem;
        margin-bottom: 16px;
      }

      .button-wrap {
        .button {
          min-width: 220px;
          min-height: 50px;
        }
      }
    }
  }
}

.is-dark {
  .error-container {
    .error-wrapper {
      .error-inner {
        .bg-number {
          opacity: 0.09;
        }
      }
    }
  }
}

@media only screen and (max-width: 767px) {
  .error-container {
    .error-wrapper {
      padding-top: 60px;

      .error-inner {
        padding: 10px;

        .bg-number {
          top: -35px;
          left: -18px;
          right: 0;
          font-size: 13rem;
        }

        img,
        svg {
          max-width: 345px;
        }
      }
    }
  }
}
</style>
