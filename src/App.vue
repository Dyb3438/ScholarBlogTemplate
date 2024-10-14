<script>
import { RouterLink, RouterView } from 'vue-router'
import { inject } from "@vercel/analytics"

export default {
  mounted() {
    inject()
  }
 
}

</script>

<template>
  <!-- <RouterView/> -->
  <RouterView v-slot="{ Component, route }">
    <transition name="slide-left">
      <component :is="Component"/>
    </transition>
</RouterView>
</template>

<style scoped>

.slide-left-enter-active,
.slide-left-leave-active,
.slide-right-enter-active,
.slide-right-leave-active {
  transition: all 0.75s ease-out;
}


.slide-left-enter-to {
  position: absolute;
  right: 0;
}


.slide-left-enter-from {
  position: absolute;
  right: -100%;
}


.slide-left-leave-to {
  position: absolute;
  left: -100%;
}


.slide-left-leave-from {
  position: absolute;
  left: 0;
}

.slide-right-enter-to {
  position: absolute;
  left: 0;
}


.slide-right-enter-from {
  position: absolute;
  left: -100%;
}


.slide-right-leave-to {
  position: absolute;
  right: -100%;
}


.slide-right-leave-from {
  position: absolute;
  right: 0;
}


</style>
