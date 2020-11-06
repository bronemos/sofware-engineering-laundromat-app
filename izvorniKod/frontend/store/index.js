import Vue from 'vue';
import axios from 'axios';

export const state = () => ({});

export const mutations = {
  SET_USER(state, user){
    state.auth.user = user;
  },
}

export const actions = {
  
  async nuxtServerInit({ commit, state, dispatch }, { app, route, req }) {
    let token = this.$auth.getToken('local')
    if (token) {
      try {
        let response = await this.$axios.get('account/logged_user_data/', {headers: {'Authorization': `${token}`}});
        commit('SET_USER', response.data.user)
      } catch(e) {
          console.log(e)
      }
    }
  },
}