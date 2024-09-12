'use strict'

const http = require('http')
const pg = require('pg')

function initRaspEndpoints (app) {
  const pool = new pg.Pool()

  app.get('/rasp/ssrf', (req, res) => {
    const clientRequest = http.get(`http://${req.query.domain}`, () => {
      res.end('end')
    })
    clientRequest.on('error', (e) => {
      if (e.name === 'DatadogRaspAbortError') {
        throw e
      }
      res.writeHead(500).end(e.message)
    })
  })

  app.post('/rasp/ssrf', (req, res) => {
    const clientRequest = http.get(`http://${req.body.domain}`, () => {
      res.end('end')
    })
    clientRequest.on('error', (e) => {
      if (e.name === 'DatadogRaspAbortError') {
        throw e
      }
      res.writeHead(500).end(e.message)
    })
  })

  app.get('/rasp/sqli', async (req, res) => {
    try {
      await pool.query(`SELECT * FROM users WHERE id='${req.query.user_id}'`)
    } catch (e) {
      if (e.name === 'DatadogRaspAbortError') {
        throw e
      }

      res.writeHead(500).end(e.message)
      return
    }

    res.end('end')
  })

  app.post('/rasp/sqli', async (req, res) => {
    try {
      await pool.query(`SELECT * FROM users WHERE id='${req.body.user_id}'`)
    } catch (e) {
      if (e.name === 'DatadogRaspAbortError') {
        throw e
      }

      res.writeHead(500).end(e.message)
      return
    }

    res.end('end')
  })
}
module.exports = initRaspEndpoints
