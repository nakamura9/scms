var path = require("path");
var webpack = require("webpack");
var BundleTracker = require("webpack-bundle-tracker");

module.exports = {
    context: __dirname,
    entry:  {
        index: './js/index',
        invoicing: './js/invoicing'
    },
    output: {
        path: path.resolve('./bundles/'),
        filename: '[name].js',
    },
    plugins: [
        new BundleTracker({filename: './webpack-stats.json'})
    ],
    mode: 'development',

    module: {
        rules: [
            {
                test: /\.js$/,
                loader: 'babel-loader',
                exclude: /node_modules/,
                query: {
                    presets: ['react']
                }
            }
        ]
    },

    resolve: {
        extensions: [ '.js', '.jsx']
    }
}