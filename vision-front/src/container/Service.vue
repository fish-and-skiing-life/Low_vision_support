<!-- App Main Structure -->
<template>
    <div class="app-default-layout">
      <template>
         
        <!-- <app-header></app-header> -->
        <router-view></router-view>
        <!-- <app-footer></app-footer> -->
      </template>
    </div>
</template>

<script>
// import Header from "Components/Header/Header.vue";
// import Footer from "Components/Footer/footer.vue";

export default {
  data() {
    return {
      loading: true
    };
  },
  components: {
    // appHeader: Header,
    // appFooter: Footer,
  },
};
</script>

<style scoped>
.app-default-layout {
  height: 100vh;
  white-space:pre-line;
}
</style>
