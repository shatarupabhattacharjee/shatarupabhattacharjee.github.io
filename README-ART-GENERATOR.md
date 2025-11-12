# Artree AI Art Generator

This is an AI-powered art reference generator for Artree's painting classes. It uses OpenAI's DALL-E to generate unique reference images based on user descriptions.

## Features

- Generate custom art references using natural language
- Download high-quality generated images
- Responsive design that works on all devices
- Secure backend API for image generation

## Prerequisites

- Node.js (v14 or higher)
- npm (comes with Node.js)
- OpenAI API key (get from https://platform.openai.com/api-keys)

## Setup Instructions

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Configure Environment Variables**
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to the `.env` file

3. **Start the Development Server**
   ```bash
   npm run dev
   ```
   The server will start on http://localhost:3000

4. **Open the Application**
   - Open `art-generator.html` in your browser
   - Make sure your browser allows CORS if you're running the frontend from a file:// URL

## Deployment

For production deployment:

1. Set up a production server (e.g., Heroku, Vercel, AWS, etc.)
2. Set the `NODE_ENV` to `production`
3. Update CORS settings in `.env` to allow only your domain
4. Consider adding rate limiting and authentication

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `PORT`: Port for the server (default: 3000)
- `CORS_ORIGIN`: Allowed origin for CORS (for development)

## Troubleshooting

- If you get CORS errors, make sure your frontend is being served from the same origin as your backend or update the CORS settings
- Check the server logs for any error messages
- Ensure your OpenAI API key has sufficient credits and the correct permissions

## License

This project is licensed under the MIT License - see the LICENSE file for details.
