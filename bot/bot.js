// bot.js
import pkg from 'whatsapp-web.js'
const { Client, LocalAuth } = pkg
import qrcode from 'qrcode-terminal'
import axios from 'axios'
import FormData from 'form-data'
import fs from 'fs'

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

client.on('qr', (qr) => {
  console.log('\nQR Code generated. Scan with WhatsApp:\n')
  qrcode.generate(qr, { small: true })
  console.log('\nOr open WhatsApp and scan the QR above ↑\n')
})

client.on('ready', () => {
  console.log('Bot is ready and connected to WhatsApp!')
  console.log('Listening for voice messages...\n')
})

client.on('authenticated', () => {
  console.log('Authentication successful')
})

client.on('auth_failure', () => {
  console.error('Authentication failed. Delete .wwebjs_auth folder and try again.')
})

client.on('disconnected', (reason) => {
  console.log('Client disconnected:', reason)
})

// Log ALL incoming messages (for debugging)
client.on('message', async (message) => {
  const timestamp = new Date().toLocaleTimeString('en-IE', { hour12: false })
  const contact = await message.getContact()
  const senderName = contact.pushname || contact.number
  
  // Log every message received
  console.log(`[${timestamp}] Message from ${senderName}: ${message.type}`)
  
  // Handle both original voice messages (ptt) and regular audio messages
  const isVoiceMessage = message.hasMedia && (message.type === 'ptt' || message.type === 'audio')
  
  if (!isVoiceMessage) {
    // Log non-voice messages but don't process them
    if (message.type === 'chat') {
      console.log(`  ↳ Text: "${message.body.substring(0, 50)}${message.body.length > 50 ? '...' : ''}"`)
    } else {
      console.log(`  ↳ Skipping (not a voice message)`)
    }
    return
  }
  
  // Process voice messages
  const isForwarded = message.isForwarded
  const source = isForwarded ? 'FORWARDED' : 'ORIGINAL'
  
  console.log(`\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`)
  console.log(`VOICE MESSAGE RECEIVED (${source})`)
  console.log(`From: ${senderName}`)
  console.log(`Time: ${timestamp}`)
  console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`)
  
  try {
    // Send immediate acknowledgement
    await message.reply('Received your voice message. Analysing for deepfake detection...')
    
    console.log('→ Downloading audio...')
    const media = await message.downloadMedia()
    const buffer = Buffer.from(media.data, 'base64')
    
    const SAVE_DIR = './collected_voice_notes'
    if (!fs.existsSync(SAVE_DIR)) fs.mkdirSync(SAVE_DIR, { recursive: true })
    const filename = `voice-${Date.now()}.ogg`
    const savePath = `${SAVE_DIR}/${filename}`
    fs.writeFileSync(savePath, buffer)
    console.log(`✓ Saved as ${savePath} (${(buffer.length / 1024).toFixed(2)} KB)`)
    
    // Send to deepfake detection API
    const form = new FormData()
    form.append('file', fs.createReadStream(savePath))
    
    console.log('→ Sending to deepfake detection model...')
    const startTime = Date.now()
    
    const res = await axios.post('http://127.0.0.1:8000/detect', form, {
      headers: form.getHeaders(),
      timeout: 30000
    })
    
    const processingTime = ((Date.now() - startTime) / 1000).toFixed(2)
    const { verdict, confidence_real, confidence_fake } = res.data
    
    console.log(`Detection complete in ${processingTime}s`)
    console.log(`  Verdict: ${verdict}`)
    console.log(`  Real: ${(confidence_real * 100).toFixed(1)}%`)
    console.log(`  Fake: ${(confidence_fake * 100).toFixed(1)}%`)
    
    // Format response message
    const emoji = verdict === 'REAL' ? '✅' : '⚠️'
    const resultMessage = 
      `${emoji} Deepfake Detection Result\n\n` +
      `Verdict: ${verdict}\n` +
      `Confidence (Real): ${(confidence_real * 100).toFixed(1)}%\n` +
      `Confidence (Fake): ${(confidence_fake * 100).toFixed(1)}%\n\n` +
      `Processed in ${processingTime}s`
    
    await message.reply(resultMessage)
    console.log('Result sent to user\n')
    
  } catch (err) {
    console.error('ERROR:', err.message)
    if (err.response) {
      console.error('  API Response:', err.response.data)
    }
    await message.reply('Sorry, deepfake detection failed. Please try again.')
  }
})

console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')
console.log('WhatsApp Deepfake Detection Bot')
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n')
console.log('→ Starting bot...\n')
client.initialize()