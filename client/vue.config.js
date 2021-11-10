module.exports = {
  publicPath: process.env.NODE_ENV === 'production' ? '../static/' : '/',
  outputDir: 'static',
  indexPath: 'index.html',
  filenameHashing: true,
  devServer: process.env.NODE_ENV === 'production' ? {} : {
    host: '127.0.0.1',
    port: 8888, // 端口号
    https: false, // https:{type:Boolean}
    open: false,
    hotOnly: true, // 热更新

    proxy: {
      '/api': {
        target: 'http://192.168.1.10:8000/',
        ws: true,
        changeOrigin: true,
        pathRewrite: {
          '^/api': '',
        },
      },
    },
  },
};
