
<template>
  <vue-iframe
    class="patho-viewer"
    :src="src"
    frame-id="my-ifram"
    @load="onLoad"
    name="my-frame"
  />
</template>

<script>
import { mapState, mapGetters, mapMutations } from 'vuex';

export default {
  name: 'MyIframe',
  data: () => ({
    myIframe: null,
    src: "http://localhost:3000/P-0014157-475886.dzi",
  }),
  methods: {
    onLoad(frame) {
      this.myIframe = frame.contentWindow
    }
  }
}
</script>


<style lang="scss" scoped>
.patho-viewer {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  flex-direction: column;
}
</style>