<script setup lang="ts">
import { ref, onBeforeMount, computed } from 'vue'
import { platformService } from '/@src/services/platformService'
import { utils } from '/@src/services/utils'

const notifications = ref([])
const filters = ref('')

const filteredData = computed(() => {
  if (!filters.value) {
    return notifications.value
  } else {
    return notifications.value.filter((item: any) => {
      return (
        item.type.match(new RegExp(filters.value, 'i')) ||
        item.content.match(new RegExp(filters.value, 'i')) ||
        item.user_name.match(new RegExp(filters.value, 'i')) ||
        item.object_type.match(new RegExp(filters.value, 'i')) ||
        item.tags.match(new RegExp(filters.value, 'i'))
      )
    })
  }
})

onBeforeMount(async () => {
  let ret = await platformService.getCurrUserNotifications()
  notifications.value = ret.results
})
</script>

<template>
  <div class="list-view-toolbar">
    <VControl icon="feather:search">
      <input v-model="filters" class="input custom-text-filter" placeholder="Search..." />
    </VControl>
    <div class="buttons">
      <VButton :to="{ name: 'home' }" icon="lnir lnir-arrow-left rem-100" light raised elevated> Home </VButton>
    </div>
  </div>
  <div class="timeline-wrapper">
    <div class="timeline-header"></div>
    <div class="timeline-wrapper-inner">
      <div class="timeline-container">
        <!--Timeline item-->
        <div v-for="item in filteredData" :key="item.id" class="timeline-item">
          <div class="date">
            <span>{{ utils.dateFmt(item.creation_date, 'MMM D, YYYY h:mm A') }}</span>
          </div>
          <div class="dot is-info"></div>
          <div class="content-wrap">
            <div class="content-box">
              <div class="status"></div>
              <VIconBox size="small" :color="utils.getNotificationColor(item.type)" rounded>
                <i class="iconify" :data-icon="utils.getNotificationImage(item.type)"></i>
              </VIconBox>

              <div class="box-text">
                <div class="meta-text">
                  <p>
                    <span>{{ item.user_name }}</span>
                  </p>
                  <span>{{ item.content }}</span>
                </div>
              </div>
              <div class="box-end">
                <VTagc
                  v-if="item.object_type"
                  :label="utils.getNotificationObjectDesc(item)"
                  color="purple"
                  rounded
                  outlined
                />
                <VTagc v-if="item.tags" :label="item.tags" color="purple" rounded outlined />
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- <div class="load-more-wrap has-text-centered">
        <VButton dark-outlined>Load More</VButton>
      </div> -->
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import '/@src/scss/abstracts/all';

/*
  1. Timeline
  2. Timeline Dark mode
  3. Media Queries
*/

/* ==========================================================================
1. Timeline
========================================================================== */
.timeline-wrapper {
  max-width: 940px;
  margin: 0 auto;

  .timeline-wrapper-inner {
    padding-top: 30px;

    .timeline-container {
      .timeline-item {
        position: relative;
        display: flex;
        align-items: center;
        margin-bottom: 10px;

        // &::before {
        //   content: '';
        //   position: absolute;
        //   top: 46px;
        //   left: 111px;
        //   height: 100%;
        //   width: 2px;
        //   background: var(--placeholder);
        //   z-index: 0;
        // }

        // &:last-child {
        //   &::before {
        //     display: none;
        //   }
        // }

        &.is-unread {
          .content-wrap {
            .content-box {
              .status {
                background: var(--red) !important;
              }
            }
          }
        }

        .date {
          width: 80px;
          font-family: var(--font);
          text-align: right;

          span {
            font-size: 0.9rem;
            color: var(--light-text);
          }
        }

        .dot {
          position: relative;
          height: 14px;
          width: 14px;
          border-radius: var(--radius-rounded);
          border: 2.6px solid var(--primary);
          margin: 0 25px;
          z-index: 1;

          &.is-info {
            border-color: var(--info);
          }

          &.is-success {
            border-color: var(--success);
          }

          &.is-warning {
            border-color: var(--warning);
          }

          &.is-danger {
            border-color: var(--danger);
          }

          &.is-purple {
            border-color: var(--purple);
          }
        }

        .content-wrap {
          @include vuer-s-card;

          flex-grow: 2;

          .content-box {
            display: flex;
            align-items: center;

            .status {
              height: 8px;
              width: 8px;
              min-width: 8px;
              border-radius: var(--radius-rounded);
              background: var(--light-text-light-15);
              margin: 0 16px 0 0;
            }

            .box-text {
              display: flex;
              align-items: center;
              justify-content: space-between;
              margin-left: 12px;
              flex-grow: 2;

              .meta-text {
                line-height: 1.2;

                p {
                  color: var(--light-text-dark-10);

                  span {
                    font-family: var(--font-alt);
                    color: var(--dark-text);
                    font-weight: 600;
                  }

                  a {
                    color: var(--primary);
                  }

                  .tag {
                    position: relative;
                    top: -1px;
                    font-weight: 500;
                    line-height: 1.8;
                    height: 1.8em;
                    margin: 0 2px;
                  }
                }

                > span {
                  color: var(--light-text);
                  font-size: 0.9rem;
                }
              }
            }

            .box-end {
              margin-left: auto;

              .v-avatar {
                margin: 0 2px;
              }
            }
          }

          .meta-content {
            padding-left: 78px;
          }
        }
      }
    }

    .load-more-wrap {
      padding: 40px 0;

      .button {
        min-width: 240px;
        min-height: 50px;
        text-transform: uppercase;
        font-size: 0.85rem;
        font-weight: 500;
        color: var(--light-text);
      }
    }
  }
}

/* ==========================================================================
2. Timeline Dark mode
========================================================================== */

.is-dark {
  .timeline-wrapper {
    .timeline-wrapper-inner {
      .timeline-container {
        .timeline-item {
          &::before {
            background: var(--dark-sidebar-light-20);
          }

          .content-wrap {
            @include vuer-card--dark;

            .content-box {
              .status {
                background: var(--dark-sidebar-light-20);
              }

              .box-text {
                .meta-text {
                  p {
                    span {
                      color: var(--dark-dark-text);
                    }

                    a {
                      color: var(--primary);
                    }
                  }
                }
              }
            }
          }
        }
      }

      .load-more-wrap {
        .button {
          background: var(--dark-sidebar-light-2) !important;
        }
      }
    }
  }
}

/* ==========================================================================
3. Media Queries
========================================================================== */

@media only screen and (max-width: 767px) {
  .timeline-wrapper {
    .timeline-wrapper-inner {
      padding-top: 0;

      .timeline-container {
        .timeline-item {
          flex-direction: column;

          &::before {
            display: none;
          }

          .dot {
            display: none;
          }

          .date {
            align-self: end;
            margin-bottom: 4px;
          }

          .content-wrap {
            .content-box {
              .box-end {
                display: none;
              }
            }
          }
        }
      }
    }
  }
}

@media only screen and (min-width: 768px) and (max-width: 1024px) and (orientation: portrait) {
  .timeline-wrapper {
    .timeline-wrapper-inner {
      padding-top: 0;

      .timeline-container {
        .timeline-item {
          flex-direction: column;

          &::before {
            display: none;
          }

          .dot {
            display: none;
          }

          .date {
            align-self: end;
            margin-bottom: 4px;
          }

          .content-wrap {
            .content-box {
              .box-end {
                display: none;
              }
            }
          }
        }
      }
    }
  }
}
</style>
