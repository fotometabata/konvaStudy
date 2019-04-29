<template>
    <div>
        <md-field>
            <label>ユーザーID</label>
            <md-input
                required
                v-model="userId"
            />
        </md-field>
        <md-field>
            <label>パスワード</label>
            <md-input
                required
                v-model="password"
                type="password"
            />
        </md-field>
        <md-button
            class="md-dense md-raised md-primary"
            @click="loggedIn"
        >
            ログイン
        </md-button>
    </div>
</template>

<script>
import Vue from 'vue';
import { mapActions } from 'vuex';

export default Vue.extend({
  name: 'Login',
  data: () => ({
    userId: '',
    password: ''
  }),
  methods: {
    ...mapActions(['SET_TOKEN', 'CHECK_TOKEN']),
    loggedIn: function() {
      let authenticate = {
        username: this.userId,
        password: this.password
      }
      this.SET_TOKEN(authenticate).then(function() {
        this.CHECK_TOKEN().then(function() {
          this.$router.push({
            name: 'hello'}
          )
        }.bind(this))
      }.bind(this))
    }
  }
})
</script>
