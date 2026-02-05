import makeWASocket, { useMultiFileAuthState, downloadMediaMessage } from 'baileys'
import fs from 'fs'
import axios from 'axios'
import QRCode from 'qrcode'
import FormData from 'form-data'

async function startBot() {
  const { state, saveCreds } = await useMultiFileAuthState('auth')

  const sock = makeWASocket({ auth: state })
  sock.ev.on('creds.update', saveCreds)

  sock.ev.on('connection.update', async ({ connection, qr }) => {
    if (qr) {
      console.log('Got QR code, generating PNG.')
      await QRCode.toFile('whatsapp-qr.png', qr)
      console.log('QR saved as whatsapp-qr.png — scan it with WhatsApp.')
    }
    if (connection === 'open') console.log('Logged in to WhatsApp!')
    if (connection === 'close') console.log('Connection closed — restart the bot.')
  })

  sock.ev.on('messages.upsert', async ({ messages }) => {
    const msg = messages[0]
    if (!msg.message) return
    const from = msg.key.remoteJid

    if (msg.message.audioMessage) {
      await sock.sendMessage(from, { text: 'Hello, thank you for your audio message. Please wait while your message is transcribed. Transcribing...' })

      try {
        const buffer = await downloadMediaMessage(msg, 'buffer')
        fs.writeFileSync('voice.ogg', buffer)

        const filename = `voice-${Date.now()}.ogg`
        fs.writeFileSync(filename, buffer)

        const form = new FormData()
        form.append('file', fs.createReadStream(filename))
        
        const res = await axios.post('http://127.0.0.1:8000/transcribe', form, {
          headers: form.getHeaders()
        })

        await sock.sendMessage(from, { text: `Transcription:\n${res.data.text}` })
      } catch (err) {
        console.error('Error processing voice note:', err)
        await sock.sendMessage(from, { text: 'Failed to transcribe your voice note.' })
      }
    }
  })
}

startBot()
