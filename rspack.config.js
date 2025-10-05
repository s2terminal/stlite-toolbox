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
      directory: path.join(__dirname), // プロジェクト全体を配信対象に
    },
    hot: true, // ホットリロード
    watchFiles: ['src/**/*', 'public/**/*'],
  },

  plugins: [
    new rspack.HtmlRspackPlugin({
      template: './public/index.html',
    }),
    new rspack.CopyRspackPlugin({
      patterns: [
        { from: 'src/src_py/streamlit_app.py', to: 'src_py/' },
        // { from: 'requirements.txt', to: '.' },
      ],
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
