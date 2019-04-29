<template>
  <div class="hello">
    <CallCanvas>
    </CallCanvas>
  </div>
</template>

<script>
import Vue from 'vue';
import CallCanvas from '../paint/CallCanvas.vue'

export default Vue.extend({
  name: 'HelloWorld',
  components: {
    CallCanvas
  },
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  }
})
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
