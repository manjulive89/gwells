'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: JSON.stringify('development'),
  APPLICATION_ROOT: process.env.APPLICATION_ROOT ? JSON.stringify(process.env.APPLICATION_ROOT) : JSON.stringify('/gwells/'),
  AXIOS_BASE_URL: process.env.AXIOS_BASE_URL ? JSON.stringify(process.env.AXIOS_BASE_URL) : JSON.stringify('/gwells/api/v1/'),
  ENABLE_DATA_ENTRY: process.env.ENABLE_DATA_ENTRY ? JSON.stringify(process.env.ENABLE_DATA_ENTRY) : JSON.stringify(true),
  // We never do analytics on dev!
  ENABLE_GOOGLE_ANALYTICS: JSON.stringify(false)
})
