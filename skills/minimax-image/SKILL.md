# MiniMax Image Generation Skill

Generate images using MiniMax's Image-01 model via their REST API.

## Usage

**Generate an image from a text prompt:**
```
Generate an image of a serene mountain landscape at sunset with vibrant orange and purple skies
```

**Generate with specific aspect ratio:**
```
Generate a product photo of a cannabis oil tincture bottle on a wooden shelf, 16:9 aspect ratio
```

**Generate multiple variations:**
```
Create 3 variations of a futuristic cityscape at night, 1:1 square format
```

## Parameters

- **prompt** (required): Text description of the desired image (max 1500 characters)
- **aspect_ratio** (optional): "1:1", "16:9", "4:3", "3:2", "2:3" — defaults to "1:1"
- **n_images** (optional): Number of images to generate (1-9) — defaults to 1
- **response_format** (optional): "url" (expires in 24h) or "base64" — defaults to "url"

## Examples

| Task | Prompt |
|------|--------|
| Product shot | "A clean product photography shot of a glass perfume bottle with soft studio lighting" |
| Landscape | "Dramatic coastline at golden hour, waves crashing against rocky cliffs, cinematic" |
| Portrait | "Stylized portrait of a woman in Art Nouveau style, warm colors, detailed ornamentation" |
| Abstract | "Geometric abstract art with flowing lines, gradient from deep blue to gold" |
| Scene | "Cozy coffee shop interior on a rainy day, warm interior lighting, steam rising from cups" |

## Output

Returns the generated image(s) as files in the workspace, with generation metadata.

## Technical Details

- Model: image-01
- Max resolution: 2048x2048
- API endpoint: POST https://api.minimax.io/v1/image_generation
- Auth: MINIMAX_API_KEY environment variable

## Notes

- Same API key as text models — no separate credentials needed
- Images with "url" format expire in 24 hours — download promptly
- Prompts work best with specific, descriptive language
