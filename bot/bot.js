// bot.js

import pkg from 'whatsapp-web.js'
const { Client, LocalAuth } = pkg
import qrcode from 'qrcode-terminal'
import axios from 'axios'
import FormData from 'form-data'
import fs from 'fs'

// Start WhatsApp client with persistent authentication and headless browser config
const client = new Client({
  authStrategy: new LocalAuth(),
  puppeteer: {
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-accelerated-2d-canvas',
      '--no-first-run',
      '--no-zygote',
      '--disable-gpu'
    ]
  }
})

// Generate QR code for first time WhatsApp authentication
client.on('qr', (qr) => {
  console.log('\nQR Code generated. Scan with WhatsApp:\n')
  qrcode.generate(qr, { small: true })
  console.log('\nOr open WhatsApp and scan the QR above\n')
})

// Confirm successful bot startup and readiness state
client.on('ready', () => {
  console.log('Bot is ready and connected to WhatsApp!')
  console.log('Listening for voice messages...\n')
})

// Log successful authentication event
client.on('authenticated', () => {
  console.log('Authentication successful')
})

// Handle authentication failures
client.on('auth_failure', () => {
  console.error('Authentication failed. Delete .wwebjs_auth folder and try again.')
})

// Log disconnections from WhatsApp session
client.on('disconnected', (reason) => {
  console.log('Client disconnected:', reason)
})

// Main message handler for all incoming WhatsApp messages
client.on('message', async (message) => {

  const timestamp = new Date().toLocaleTimeString('en-IE', { hour12: false })
  const contact = await message.getContact()
  const senderName = contact.pushname || contact.number

  // Log every incoming message type for debugging and monitoring
  console.log(`[${timestamp}] Message from ${senderName}: ${message.type}`)

  // Detect whether message contains voice or audio data
  const isVoiceMessage = message.hasMedia && (message.type === 'ptt' || message.type === 'audio')

  // Ignore non voice messages and only log text previews
  if (!isVoiceMessage) {
    if (message.type === 'chat') {
      console.log(`Text: "${message.body.substring(0, 50)}${message.body.length > 50 ? '...' : ''}"`)
    } else {
      console.log(`Skipping - not a voice message`)
    }
    return
  }

  // Extract metadata for voice message classification and logging
  const isForwarded = message.isForwarded
  const source = isForwarded ? 'FORWARDED' : 'ORIGINAL'

  console.log(`\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`)
  console.log(`VOICE MESSAGE RECEIVED (${source})`)
  console.log(`From: ${senderName}`)
  console.log(`Time: ${timestamp}`)
  console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`)

  try {

    // Acknowledge receipt to user before processing begins
    await message.reply('Received your voice message. Analysing for deepfake detection...')

    console.log('Downloading audio...')

    // Download voice message from WhatsApp
    const media = await message.downloadMedia()
    const buffer = Buffer.from(media.data, 'base64')

    console.log(`Audio size: ${(buffer.length / 1024).toFixed(2)} KB`)

    // Prepare form data for backend API request
    const form = new FormData()
    form.append('file', buffer, {
      filename: 'audio.ogg',
      contentType: 'audio/ogg'
    })

    console.log('Sending to deepfake detection model...')

    const startTime = Date.now()

    // Send audio to FastAPI backend for inference
    const res = await axios.post('http://127.0.0.1:8000/detect', form, {
      headers: form.getHeaders(),
      timeout: 30000
    })

    const processingTime = ((Date.now() - startTime) / 1000).toFixed(2)

    const { verdict, confidence_real, confidence_fake } = res.data

    // Log model inference results for debugging and monitoring
    console.log(`Detection complete in ${processingTime}s`)
    console.log(`  Verdict: ${verdict}`)
    console.log(`  Real: ${(confidence_real * 100).toFixed(1)}%`)
    console.log(`  Fake: ${(confidence_fake * 100).toFixed(1)}%`)

    // Format and send result message back to WhatsApp user
    const resultMessage =
      `Deepfake Detection Result\n\n` +
      `Verdict: ${verdict}\n` +
      `Confidence (Real): ${(confidence_real * 100).toFixed(1)}%\n` +
      `Confidence (Fake): ${(confidence_fake * 100).toFixed(1)}%\n\n` +
      `Processed in ${processingTime}s`

    await message.reply(resultMessage)

    console.log('Result sent to user\n')

  } catch (err) {

    // Handle failures from API request or processing
    console.error('ERROR:', err.message)

    if (err.response) {
      console.error('  API Response:', err.response.data)
    }

    await message.reply('Sorry, deepfake detection failed. Please try again.')
  }
})

// Initial startup logs and bot initialization
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
console.log('WhatsApp Deepfake Detection Bot')
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')
console.log('Starting bot...\n')

client.initialize()