// rspack.config.js
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  mode: 'development',
  entry: './src_js/index.js',
  devServer: {
    static: {
      directory: path.join(__dirname), // プロジェクト全体を配信対象に
    },
    hot: true, // ホットリロード
    watchFiles: ['src_js/**/*', 'src_py/**/*', 'public/**/*'],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './public/index.html',
    }),
  ],

  // .py ファイルをビルド対象から除外
  module: {
    rules: [
      {
        test: /\.py$/,
        type: 'asset/source', // .pyファイルをテキストとして扱う
      },
    ],
  },
};
