const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  // devServer: {
  //     proxy: {
  //       '^/api': {
  //         target: 'http://back:9000',
  //         changeOrigin: true
  //       },
  //     }
  //   }
})
