<template>
  <iframe
    id="iframeContain"
    name="iframeContain"
    seamless
    scrolling="yes"
    src="http://192.168.101.105:8899/spoon/spoon"
  >
  </iframe>

</template>

<script>
  export default {
    name: 'EtlPage'
  }
</script>

<style scoped>
  /** iframe样式 */
  #iframeContain{
    width: 100%;
    height: 800px;
  }
</style>