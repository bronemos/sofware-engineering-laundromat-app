
export default {
  mode: 'universal',
  /*
  ** Headers of the page
  */
  head: {
    title: process.env.npm_package_name || '',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: process.env.npm_package_description || '' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },
  /*
  ** Customize the progress-bar color
  */
  loading: { color: '#fff' },
  /*
  ** Global CSS
  */
  css: [
  ],
  /*
  ** Plugins to load before mounting the App
  */
  plugins: [
    { src: '~plugins/vue-cal.js', srr: false }
    // { src: '~plugins/vuetify.js', srr: false }
  ],
  /*
  ** Nuxt.js dev-modules
  */
  buildModules: [
    '@nuxtjs/vuetify'
  ],
  /*
  ** Nuxt.js modules
  */
  modules: [
    // Doc: https://bootstrap-vue.js.org
    'bootstrap-vue/nuxt',
    // Doc: https://axios.nuxtjs.org/usage
    '@nuxtjs/axios',
    '@nuxtjs/toast',
    '@nuxtjs/auth',
  ],
  /*
  ** Axios module configuration
  ** See https://axios.nuxtjs.org/options
  */
  axios: {
    baseURL: 'http://localhost:8000/api/'
  },
  //auth configuration
  auth: {
    strategies: {
      local: {
        endpoints: {
          login: { url: 'token-auth/', method: 'post', propertyName: 'token' },
          user: { url: 'account/logged_user_data/', method: 'get', propertyName: 'user' },
          logout: false,
        },
        tokenType: 'Token',
      }
    },
    redirect: {
      login: '/prijava',
    }
  },
  /*
  ** Build configuration
  */
  build: {  
    transpile: ['vue-cal'],
    /*
    ** You can extend webpack config here
    */
    extend (config, ctx) {
    }
  }
}
