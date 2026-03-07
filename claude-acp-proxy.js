#!/usr/bin/env node
/**
 * Claude Code ACP Proxy
 * Exposes Claude Code as an OpenAI-compatible endpoint
 * 
 * Run: node claude-acp-proxy.js
 * Endpoint: http://localhost:11434/v1/chat/completions
 */

const http = require('http');
const { spawn } = require('child_process');

const PORT = process.env.PORT || 11435;
const ACPX_PATH = process.env.ACPX_PATH || '/opt/homebrew/lib/node_modules/openclaw/extensions/acpx/node_modules/.bin/acpx';
const SESSION_NAME = process.env.SESSION_NAME || 'oc-proxy-session';

let sessionId = null;

// Ensure session exists
async function ensureSession() {
  return new Promise((resolve, reject) => {
    const proc = spawn(ACPX_PATH, ['claude', 'sessions', 'new', '--name', SESSION_NAME], {
      stdio: 'pipe'
    });
    
    let output = '';
    proc.stdout.on('data', (data) => { output += data.toString(); });
    proc.stderr.on('data', (data) => { output += data.toString(); });
    
    proc.on('close', (code) => {
      // Extract session ID from output like "created session ... (uuid)"
      const match = output.match(/\(([a-f0-9-]+)\)/);
      if (match) {
        sessionId = match[1];
        resolve(sessionId);
      } else if (sessionId) {
        resolve(sessionId);
      } else {
        // Session might already exist, try to continue
        resolve(SESSION_NAME);
      }
    });
  });
}

// Send prompt to Claude via acpx
async function claudePrompt(prompt) {
  return new Promise((resolve, reject) => {
    const args = ['claude', '-s', SESSION_NAME];
    
    // Add the prompt
    args.push(prompt);
    
    const proc = spawn(ACPX_PATH, args, {
      stdio: 'pipe',
      cwd: process.cwd()
    });
    
    let output = '';
    let errorOutput = '';
    
    proc.stdout.on('data', (data) => { output += data.toString(); });
    proc.stderr.on('data', (data) => { errorOutput += data.toString(); });
    
    proc.on('close', (code) => {
      // Extract just the assistant response, not the acpx logs
      // Look for text after [done] or end_turn markers
      const lines = output.split('\n');
      const responseLines = [];
      let inResponse = false;
      let foundEnd = false;
      
      for (const line of lines) {
        // Skip acpx status lines
        if (line.startsWith('[acpx]') || line.startsWith('[client]') || line.startsWith('[error]')) {
          continue;
        }
        // Found end marker
        if (line.includes('[done]') || line.includes('end_turn')) {
          foundEnd = true;
          break;
        }
        // Collect response lines
        if (line.trim()) {
          inResponse = true;
          responseLines.push(line);
        }
      }
      
      const response = responseLines.join('\n').trim();
      console.log('Response:', response.substring(0, 100) + '...');
      resolve(response || 'No response');
    });
    
    proc.on('error', reject);
  });
}

// Parse OpenAI request to Claude prompt
function parseRequest(body) {
  const data = JSON.parse(body);
  const messages = data.messages || [];
  
  // Build a conversation prompt
  let prompt = '';
  
  for (const msg of messages) {
    const role = msg.role;
    const content = msg.content;
    
    if (role === 'system') {
      prompt += `System: ${content}\n\n`;
    } else if (role === 'user') {
      prompt += `User: ${content}\n\n`;
    } else if (role === 'assistant') {
      prompt += `Assistant: ${content}\n\n`;
    }
  }
  
  return prompt.trim();
}

// Build OpenAI response
function buildResponse(content) {
  return {
    id: `chatcmpl-${Date.now()}`,
    object: 'chat.completion',
    created: Math.floor(Date.now() / 1000),
    model: 'claude',
    choices: [
      {
        index: 0,
        message: {
          role: 'assistant',
          content: content
        },
        finish_reason: 'stop'
      }
    ],
    usage: {
      prompt_tokens: 0,
      completion_tokens: 0,
      total_tokens: 0
    }
  };
}

// HTTP Server
const server = http.createServer(async (req, res) => {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }
  
  // Only handle POST /v1/chat/completions
  if (req.method === 'POST' && req.url === '/v1/chat/completions') {
    let body = '';
    
    req.on('data', chunk => { body += chunk; });
    req.on('end', async () => {
      try {
        const prompt = parseRequest(body);
        console.log('Prompt:', prompt.substring(0, 100) + '...');
        
        const response = await claudePrompt(prompt);
        console.log('Response:', response.substring(0, 100) + '...');
        
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(buildResponse(response)));
      } catch (err) {
        console.error('Error:', err.message);
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: { message: err.message } }));
      }
    });
  } else if (req.method === 'GET' && req.url === '/v1/models') {
    // OpenAI models endpoint
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      object: 'list',
      data: [
        {
          id: 'claude',
          object: 'model',
          created: Math.floor(Date.now() / 1000),
          owned_by: 'anthropic'
        }
      ]
    }));
  } else {
    res.writeHead(404);
    res.end('Not found');
  }
});

// Start server
async function main() {
  console.log('Ensuring Claude session exists...');
  await ensureSession();
  console.log(`Session ready: ${SESSION_NAME}`);
  
  server.listen(PORT, () => {
    console.log(`Claude ACP Proxy running at http://localhost:${PORT}/v1/chat/completions`);
  });
}

main().catch(console.error);
