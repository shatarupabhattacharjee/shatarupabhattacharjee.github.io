import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import { fileURLToPath } from 'url';
import { dirname, join, basename } from 'path';
import { writeFile, mkdir, readFile } from 'fs/promises';
import fs from 'fs';
import { spawn } from 'child_process';
import fetch from 'node-fetch';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Ensure uploads directory exists
const uploadsDir = join(__dirname, 'public', 'generated');
mkdir(uploadsDir, { recursive: true });

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.status(200).json({ status: 'ok', message: 'Artree AI Generator is running with Ollama' });
});

// Serve the placeholder image directly
app.get('/placeholder.svg', (req, res) => {
  res.sendFile(join(__dirname, 'public', 'placeholder.svg'));
});

// Generate art reference using LLaVA with placeholder image
app.post('/api/generate-image', async (req, res) => {
  try {
    const { prompt } = req.body;

    if (!prompt) {
      return res.status(400).json({ error: 'Prompt is required' });
    }

    // Get the art description using LLaVA
    const llavaResponse = await fetch('http://localhost:11434/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: 'llava',
        prompt: `Create a detailed painting reference for: ${prompt}.\n\n` +
                `Include:\n` +
                `1. Composition notes\n` +
                `2. Color palette suggestions\n` +
                `3. Style recommendations\n` +
                `4. Mood and atmosphere\n` +
                `5. Lighting conditions\n` +
                `6. Key elements to focus on\n\n` +
                `Make it detailed and helpful for an artist.`,
        stream: false,
      }),
    });

    if (!llavaResponse.ok) {
      console.error('LLaVA API error:', await llavaResponse.text());
      throw new Error(`LLaVA API error: ${llavaResponse.statusText}`);
    }

    const llavaResult = await llavaResponse.json();
    const description = llavaResult.response || 'No description generated';
    
    // Save the description to a text file
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const descFilename = `description-${timestamp}.txt`;
    const descFilepath = join(uploadsDir, descFilename);
    await writeFile(descFilepath, description, 'utf-8');

    // Use the placeholder image with absolute URL
    const placeholderImage = '/placeholder.svg';

    res.json({ 
      success: true, 
      textResponse: description,
      imageUrl: placeholderImage,
      prompt: prompt,
      timestamp: new Date().toISOString(),
      isPlaceholder: true
    });

  } catch (error) {
    console.error('Error generating art reference:', error);
    res.status(500).json({ 
      success: false, 
      error: 'Failed to generate art reference',
      details: error.message
    });
  }
});

// Serve static files
app.use(express.static('public'));

// Start server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server is running on http://localhost:${PORT}`);
  console.log('Make sure Ollama is running with the LLaVA model installed');
  console.log('Run: ollama pull llava');
});

// Handle unhandled promise rejections
process.on('unhandledRejection', (err) => {
  console.error('Unhandled Rejection:', err);
  process.exit(1);
});
