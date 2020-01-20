<template>
  <div>
    <chat />
    <hero />
    <hr />
    <home-content />
  </div>
</template>

<script>
import Hero from "../components/Hero";
import HomeContent from "../components/HomeContent";
import Chat from "../components/Chat"

export default {
  name: "home",
  components: {
    Chat,
    Hero,
    HomeContent
  }
};
</script>

<style lang="scss" scoped>
.next-steps {
  .fa-link {
    margin-right: 5px;
  }
}
</style>
