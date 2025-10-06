// rspack.config.js
const path = require('path');
const rspack = require('@rspack/core');

module.exports = {
  mode: process.env.NODE_ENV === 'production' ? 'production' : 'development',
  entry: './src/index.js',

  // ビルド設定
  output: {
    filename: '[name].[contenthash].js',
    path: path.resolve(__dirname, 'dist'),
    publicPath: 'auto', // GitHub Pagesのサブディレクトリに対応
    clean: true,
  },

  // 開発サーバー設定
  devServer: {
    static: {
      directory: path.join(__dirname, 'public'),
    },
    hot: true, // ホットリロード
    watchFiles: ['src/**/*', 'public/**/*'],
    open: true,
  },

  plugins: [
    new rspack.HtmlRspackPlugin({
      template: './public/index.html',
    }),
    new rspack.CopyRspackPlugin({
      patterns: [
        {
          from: 'public/src_py',
          to: 'src_py',
        },
      ],
    }),
  ],
};
