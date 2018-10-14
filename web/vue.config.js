const path = require('path')
const BundleTracker  = require('webpack-bundle-tracker')

function resolve (dir) {
  return path.join(__dirname, '..', dir)
}

module.exports = {
  assetsDir: 'static',

  devServer: {
    headers: {
        "Access-Control-Allow-Origin":"\*"
    },
  },

  configureWebpack: {

    output: {
        filename: "[name]-[hash].js",
    },

    plugins: [
      new BundleTracker({
        path: __dirname,
        publicPath: "http://localhost:8080/",
        filename: './webpack-stats.json'
      })
    ]
  }
}
