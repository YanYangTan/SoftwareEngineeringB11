module.exports = {
  publicPath: process.env.NODE_ENV === 'production'? '../static/' : '/',
  outputDir: 'static',
  indexPath: 'index.html',
  filenameHashing: true,
  devServer: process.env.NODE_ENV === 'production'? {} : {
    host: "0.0.0.0",
		port: 8024, // 端口号
		https: false, // https:{type:Boolean}
		open: false,
		hotOnly: true, // 热更新

    proxy: {
          '/api': {
            target: 'http://82.156.102.67:8000/',
            ws: true,
            changeOrigin: true,
            pathRewrite: {
                "^/api": ""
            }
          }
    }
  }
}
