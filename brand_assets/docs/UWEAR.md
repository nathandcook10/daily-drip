# UWEAR.md

Agent-ready reference for using the Uwear AI API.

## Core Rules

- Base URL: `https://api.uwear.ai`
- Authenticate documented routes with `Authorization: Bearer YOUR_API_KEY`.
- API keys authenticate selected internal Uwear routes directly; legacy `/api/v1` aliases are not used for generation, clothing, avatar, or result operations.
- Requests and responses use `snake_case` field names.
- Create generation jobs with `POST /generation`, then poll `GET /generation/{generation_id}` until the status is `Done`, `Error`, `Created`, or `Ongoing`.
- Webhook callbacks can replace polling. Configure a saved endpoint on the API Keys page or send request-level webhook fields; terminal webhook payloads put generated assets in `data.results`.
- Polling responses from generation routes put generated assets in `generation_results`.
- Generated assets are available for 4 hours. Download and persist any URLs you need.
- Credits are consumed per request based on model, output count, resolution, duration, and audio options.

## Getting Started

1. Create or retrieve an API key from the Uwear API keys page.
2. Purchase credits before submitting generation jobs.
3. Create clothing items first for try-on workflows, then reference their IDs in generation requests.

## Request Workflow

1. Create a generation request with `POST /generation`.
2. Poll `GET /generation/{generation_id}` for status, or wait for `generation.completed` / `generation.failed` webhooks.
3. For polling, read `generation_results`. For webhooks, read `data.results`. Download result URLs before they expire.

## Agent Workflow Guide

Use this section before the endpoint reference. It describes how an agent should plan real fashion workflows with the documented API surface only.

### Core Agent Pattern

1. Clarify the user's production goal: single image, collection shoot, ecommerce try-on, edit, upscale, video, or a chained workflow.
2. Create or reuse structured assets first: clothing items for garments, avatars for consistent models, and generation results for follow-up edits, upscales, or videos.
3. Submit generation jobs with explicit settings instead of vague prompts: `model_slug`, `use_case`, `camera`, `aspect_ratio`, `resolution`, `num_images`, and `avatar_id` when needed.
4. Wait for completion through polling for small local scripts or webhooks for production and bulk workflows.
5. Download and persist result URLs within 4 hours. Treat Uwear result URLs as temporary delivery URLs, not permanent storage.
6. Keep an external manifest that maps each user-facing asset back to its SKU, clothing item, generation ID, result ID, prompt, model, camera, and final stored URL.

### Best Practice: Generate a Whole Collection in Bulk

Do not try to describe an entire collection in one prompt. Treat a collection as many structured generation jobs that share a consistent creative brief.

Recommended plan:

1. Build a catalog manifest with one row per garment or outfit. Include at minimum: `sku`, `name`, `front_image_url`, optional `back_image_url`, `prompt`, `camera`, `model_slug`, `aspect_ratio`, `resolution`, and `num_images`.
2. Create or find one clothing item per garment before generation. Reuse existing `clothing_item_id` values when the garment was already uploaded.
3. Use a shared collection brief for consistency, then add SKU-specific details only when they matter. Example: same model casting, same lighting, same background family, same crop, different garment.
4. Submit one documented `POST /generation` job per garment, outfit, camera, or creative variant. For very large catalogs, process in controlled chunks and track each submitted `generation_id` in your manifest.
5. Prefer webhooks for collection-scale work. If polling, poll with backoff and stop when each job reaches `Done` or `Error`.
6. Persist every completed result immediately to your own storage, DAM, PIM, Shopify app, or product database before the 4-hour URL window closes.
7. Retry only failed or missing rows. Use your manifest for idempotency so reruns do not duplicate successful generations.

Collection quality guidance:

- Keep `camera`, `aspect_ratio`, and `resolution` stable across the collection unless the user asks for deliberate variation.
- Generate a small pilot set first, review outputs, then scale the same settings to the full catalog.
- Use saved avatars when brand/model consistency matters across many SKUs.
- Avoid changing model, prompt style, camera, and resolution all at once; it makes quality problems hard to diagnose.
- Store rejected outputs too when useful, but mark approval status in your own manifest rather than relying only on generation history.

### Best Practice: Implement Virtual Try-On on a Platform

Use the documented generation flow as the open API foundation for platform try-on experiences. Keep API keys on your backend; never expose a Uwear API key in browser, mobile, or client-side storefront code.

Recommended architecture:

1. Product setup: map each product or variant in your catalog to a Uwear clothing item. Store `clothing_item_id` beside your SKU or product ID.
2. User/model setup: if the experience uses a persistent shopper or brand model, create or reuse an avatar only with the user's permission and clear retention rules.
3. Try-on request: your frontend sends product, user/model choice, and desired view to your backend. Your backend calls Uwear with the mapped `clothing_item_id`, optional `avatar_id`, and a clear try-on prompt.
4. Completion: your backend either polls the generation status or receives a webhook, then updates your frontend, database, or queue with the completed result.
5. Delivery: copy final images to your own storage if they must remain visible after the temporary Uwear URL expires.
6. Privacy and consent: disclose AI generation, avoid uploading user images without consent, and provide deletion or refresh paths for saved avatars or generated try-on assets.

Try-on prompt guidance:

- Describe the model and context, not the garment anatomy already captured by the clothing item.
- Keep ecommerce try-on prompts practical: full body or relevant crop, clean lighting, neutral background, garment visible, no distracting accessories unless requested.
- Use saved avatars for consistency. Use a virtual model when the user does not need personal identity or shopper-specific fitting.
- For production storefronts, design for asynchronous completion: show progress, allow retry, and handle failed generations gracefully.

### Best Practice: Chain Image, Edit, Upscale, and Video

Many useful fashion workflows are chains rather than single generations.

1. Generate candidate product images with `use_case=generate`.
2. Pick approved result IDs in your own workflow or UI.
3. Use approved results as the source for `use_case=edit`, `use_case=upscale`, or `use_case=video`.
4. Keep parent-child relationships in your own manifest so an agent can explain where each final asset came from.

### Agent Guardrails

- Use only routes documented in this file unless the user explicitly provides another Uwear contract.
- Do not invent batch, Shopify, widget, private, admin, or mobile routes from assumptions.
- Do not put API keys in frontend code, screenshots, logs, prompts, or generated files.
- Do not promise exact body fit, sizing accuracy, or shopper measurement inference unless the user has a dedicated Uwear sizing/try-on integration contract.
- When unsure about rate limits, concurrency, or commercial constraints, build a queue with conservative concurrency and ask the user to confirm their account limits.


## Clothing Items
Manage your digital wardrobe by creating, retrieving, updating, and deleting clothing items. Upload images of your clothing and let our AI vision model help generate accurate descriptions for better generation results.

### GET /clothing-items
**List Clothing Items**
Retrieve a paginated list of all your clothing items. This operation takes longer to complete than getting a single clothing item.

#### Parameters
| Name | Location | Required | Type | Default | Allowed values | Description |
| --- | --- | --- | --- | --- | --- | --- |
| page | query | no | integer |  |  | Page number for pagination |
| items_per_page | query | no | integer |  |  | Number of items per page |


#### Example Request

```json
{
  "page": "1",
  "items_per_page": "20"
}
```


#### Example Response

```json
{
  "current_page": 1,
  "max_page": 3,
  "total_count": 45,
  "data": [
    {
      "clothing_item_id": 123,
      "clothing_item_name": "One-Piece Swimsuit",
      "description": "Swimsuit with narrow shoulder straps, color-blocked design featuring red, blue, and white sections, large rectangular graphic with navy border and 'Tommy Hilfiger' signature in black, fitted silhouette.",
      "description_back": "Blue swimsuit, low back design, thin straps in turquoise, contrast color detail at the waistband in red, smooth fabric texture, full coverage bottom.",
      "clothing_item_url": "https://app-uwear-prod.s3.us-east-1.amazonaws.com/clothing-items/8613/f20d267c4cc24a6b8539481444801c52.png",
      "clothing_item_back_url": "https://app-uwear-prod.s3.us-east-1.amazonaws.com/clothing-items/8613/bf08b837790846be8cb5ff47dd2f4ae2.png",
      "external_clothing_item_url": "",
      "external_clothing_item_back_url": "",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```


### POST /clothing-item
**Create New Clothing Item**
Create a new clothing item by providing image URLs or uploaded files. This internal route accepts API keys and uses form data, matching the route used by the Uwear app.

Content-Type: `multipart/form-data`

#### Request Body Parameters
| Name | Location | Required | Type | Default | Allowed values | Description |
| --- | --- | --- | --- | --- | --- | --- |
| clothing_item_name | body | yes | string |  |  | User-friendly name for your clothing item |
| description | body | no | string |  |  | Description of the front view. Auto-generated by AI vision, but you can provide additional details for features not visible in the image (e.g., "oversized fit", "slim cut", "high waist") |
| description_back | body | no | string |  |  | Description of the back view. Auto-generated by AI vision, but you can provide additional details to improve generation accuracy |
| clothing_item_url | body | yes | string |  |  | Image URL of the front of your clothing item |
| clothing_item_back_url | body | no | string |  |  | Image URL of the back of your clothing item. Optional - if not provided, front image will be used for back shot generations |
| use_image_enhancement | body | no | boolean | true |  | Enable AI processing to remove backgrounds and generate descriptions (1 credit). Default: true. Set to false only with clean flat lay photos and complete descriptions |


#### Example Request

```json
{
  "clothing_item_name": "Vintage Denim Jacket",
  "description": "Classic blue denim jacket with brass buttons, chest pockets, and a slightly oversized fit",
  "description_back": "Adjustable waist tabs at the back for a customized fit",
  "clothing_item_url": "https://example.com/denim-jacket-front.jpg",
  "clothing_item_back_url": "https://example.com/denim-jacket-back.jpg",
  "use_image_enhancement": true
}
```


#### Example Response

```json
{
  "clothing_item_id": 123,
  "clothing_item_name": "One-Piece Swimsuit",
  "description": "Swimsuit with narrow shoulder straps, color-blocked design featuring red, blue, and white sections, large rectangular graphic with navy border and 'Tommy Hilfiger' signature in black, fitted silhouette.",
  "description_back": "Blue swimsuit, low back design, thin straps in turquoise, contrast color detail at the waistband in red, smooth fabric texture, full coverage bottom.",
  "clothing_item_url": "https://app-uwear-prod.s3.us-east-1.amazonaws.com/clothing-items/8613/f20d267c4cc24a6b8539481444801c52.png",
  "clothing_item_back_url": "https://app-uwear-prod.s3.us-east-1.amazonaws.com/clothing-items/8613/bf08b837790846be8cb5ff47dd2f4ae2.png",
  "external_clothing_item_url": "",
  "external_clothing_item_back_url": "",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```


### GET /clothing-item/{clothing_item_id}
**Get Clothing Item Details**
Get detailed information about a specific clothing item by its ID, including its name, description, and images used as input for the generation.

#### Parameters
| Name | Location | Required | Type | Default | Allowed values | Description |
| --- | --- | --- | --- | --- | --- | --- |
| clothing_item_id | path | yes | integer |  |  | The ID of the clothing item to retrieve |


#### Example Request

```json
{
  "clothing_item_id": "123"
}
```


#### Example Response

```json
{
  "clothing_item_id": 123,
  "clothing_item_name": "One-Piece Swimsuit",
  "description": "Swimsuit with narrow shoulder straps, color-blocked design featuring red, blue, and white sections, large rectangular graphic with navy border and 'Tommy Hilfiger' signature in black, fitted silhouette.",
  "description_back": "Blue swimsuit, low back design, thin straps in turquoise, contrast color detail at the waistband in red, smooth fabric texture, full coverage bottom.",
  "clothing_item_url": "https://app-uwear-prod.s3.us-east-1.amazonaws.com/clothing-items/8613/f20d267c4cc24a6b8539481444801c52.png",
  "clothing_item_back_url": "https://app-uwear-prod.s3.us-east-1.amazonaws.com/clothing-items/8613/bf08b837790846be8cb5ff47dd2f4ae2.png",
  "external_clothing_item_url": "",
  "external_clothing_item_back_url": "",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```


### PUT /clothing-item/{clothing_item_id}
**Update Clothing Item**
Update the name and descriptions of an existing clothing item. Note: To update images, create a new clothing item with the desired images.

#### Parameters
| Name | Location | Required | Type | Default | Allowed values | Description |
| --- | --- | --- | --- | --- | --- | --- |
| clothing_item_id | path | yes | integer |  |  | The ID of the clothing item to update |


#### Request Body Parameters
| Name | Location | Required | Type | Default | Allowed values | Description |
| --- | --- | --- | --- | --- | --- | --- |
| clothing_item_name | body | no | string |  |  | User-friendly name for your clothing item |
| description | body | no | string |  |  | Description of the front view. Auto-generated by AI vision, but you can provide additional details for features not visible in the image (e.g., "oversized fit", "slim cut", "high waist") |
| description_back | body | no | string |  |  | Description of the back view. Auto-generated by AI vision, but you can provide additional details to improve generation accuracy |
| clothing_item_url | body | no | string |  |  | Image URL of the front of your clothing item |
| clothing_item_back_url | body | no | string |  |  | Image URL of the back of your clothing item. Optional - if not provided, front image will be used for back shot generations |


#### Example Request

```json
{
  "clothing_item_id": "123",
  "clothing_item_name": "Vintage Floral Summer Dress",
  "description": "A vintage-inspired floral pattern summer dress with a flowing A-line silhouette and short sleeves",
  "description_back": "Features a concealed zipper closure and vintage-style button details at the back",
  "clothing_item_url": "https://example.com/floral-dress-front.jpg",
  "clothing_item_back_url": "https://example.com/floral-dress-back.jpg"
}
```


#### Example Response

```json
{
  "clothing_item_id": 123,
  "clothing_item_name": "One-Piece Swimsuit",
  "description": "Swimsuit with narrow shoulder straps, color-blocked design featuring red, blue, and white sections, large rectangular graphic with navy border and 'Tommy Hilfiger' signature in black, fitted silhouette.",
  "description_back": "Blue swimsuit, low back design, thin straps in turquoise, contrast color detail at the waistband in red, smooth fabric texture, full coverage bottom.",
  "clothing_item_url": "https://app-uwear-prod.s3.us-east-1.amazonaws.com/clothing-items/8613/f20d267c4cc24a6b8539481444801c52.png",
  "clothing_item_back_url": "https://app-uwear-prod.s3.us-east-1.amazonaws.com/clothing-items/8613/bf08b837790846be8cb5ff47dd2f4ae2.png",
  "external_clothing_item_url": "",
  "external_clothing_item_back_url": "",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```


### DELETE /clothing-item/{clothing_item_id}
**Delete Clothing Item**
Delete a clothing item by its ID. This operation will also delete all associated generations and generation results and is irreversible.

#### Parameters
| Name | Location | Required | Type | Default | Allowed values | Description |
| --- | --- | --- | --- | --- | --- | --- |
| clothing_item_id | path | yes | integer |  |  | The ID of the clothing item to delete |


#### Example Request

```json
{
  "clothing_item_id": "123"
}
```


#### Example Response

```json
{
  "message": "Clothing item deleted successfully"
}
```


## Generation Requests
Create and manage AI-powered clothing generations. Generate photorealistic images of your clothing items on virtual models or avatars with various poses, camera angles, and backgrounds.

### GET /generations
**Get All Generations**
Retrieve a paginated list of your generation requests with filtering options.

#### Parameters
| Name | Location | Required | Type | Default | Allowed values | Description |
| --- | --- | --- | --- | --- | --- | --- |
| status | query | no | string |  | Done, Created, Ongoing, Error | Filter by status: Done (completed), Created (queued), Ongoing (processing), or Error (failed) |
| feature_name | query | no | string |  |  | Filter by feature/model name |
| external_id | query | no | string |  |  | Filter by the provider's external job ID |
| batch_id | query | no | integer |  |  | Filter by batch ID |
| sort | query | no | string | created_at:desc |  | Sort order, for example created_at:desc |
| page | query | no | integer |  |  | Page number for pagination |
| items_per_page | query | no | integer |  |  | Number of items per page |


#### Example Request

```json
{
  "status": "Done",
  "sort": "created_at:desc",
  "page": "1",
  "items_per_page": "10"
}
```


#### Example Response

```json
{
  "current_page": 1,
  "max_page": 5,
  "total_count": 48,
  "data": [
    {
      "generation_id": 789,
      "clothing_item_id": 123,
      "num_images": 2,
      "payload": "{\"prompt\": \"Young woman with brown hair wearing the dress in a sunny garden\", \"camera\": \"photo\"}",
      "status": "Done",
      "feature_name": "nano_banana_pro_clothing",
      "created_at": "2024-01-15T15:30:00Z",
      "updated_at": "2024-01-15T15:32:00Z",
      "avatar_id": null,
      "generation_results": [
        {
          "generation_result_id": 1234,
          "generation_id": 789,
          "url": "https://app-uwear-prod.s3.us-east-1.amazonaws.com/generation-results/8613/image/test_otto_464661.png",
          "kind": "Image",
          "created_at": "2024-01-15T15:32:00Z",
          "updated_at": null,
          "clothing_item_id": 123,
          "available": true,
          "origin": "api"
        }
      ]
    }
  ]
}
```


### GET /generation/{generation_id}
**Get Generation Details**
Get detailed information about a specific generation by its ID, including its status, settings, and results. Polling responses return generated assets in generation_results; webhook callbacks return terminal assets in data.results.

#### Parameters
| Name | Location | Required | Type | Default | Allowed values | Description |
| --- | --- | --- | --- | --- | --- | --- |
| generation_id | path | yes | integer |  |  | The ID of the generation to retrieve |


#### Example Request

```json
{
  "generation_id": "789"
}
```


#### Example Response

```json
{
  "generation_id": 789,
  "clothing_item_id": 123,
  "num_images": 2,
  "payload": "{\"prompt\": \"Woman wearing a one-piece swimsuit on the beach\", \"camera\": \"photo\", \"generation_setting\": {\"color_hex\": \"#ffffff\", \"retries_for_duplicates\": false}}",
  "status": "Done",
  "feature_name": "nano_banana_pro_clothing",
  "created_at": "2024-01-15T15:30:00Z",
  "updated_at": "2024-01-15T15:32:00Z",
  "avatar_id": null,
  "generation_results": [
    {
      "generation_result_id": 1567,
      "generation_id": 789,
      "url": "https://app-uwear-prod.s3.us-east-1.amazonaws.com/generation-results/8613/image/test_zapier_403485.png",
      "kind": "Image",
      "created_at": "2024-01-15T15:31:00Z",
      "updated_at": "2024-01-15T15:31:00Z",
      "clothing_item_id": 123,
      "available": true,
      "origin": "api"
    },
    {
      "generation_result_id": 1568,
      "generation_id": 789,
      "url": "https://app-uwear-prod.s3.us-east-1.amazonaws.com/generation-results/8613/image/test_zapier_284171.png",
      "kind": "Image",
      "created_at": "2024-01-15T15:32:00Z",
      "updated_at": "2024-01-15T15:32:00Z",
      "clothing_item_id": 123,
      "available": true,
      "origin": "api"
    }
  ]
}
```


### POST /generation
**Create Generation**
Create a generation job using the same internal route as the Uwear app. Use this route for try-on images, edits, upscales, and video jobs by setting use_case and the relevant source fields. Configure a saved webhook on the API Keys page or send a request-level webhook_url to receive terminal callbacks with results in data.results.

#### Request Body Parameters
| Name | Location | Required | Type | Default | Allowed values | Description |
| --- | --- | --- | --- | --- | --- | --- |
| clothing_item_id | body | no | integer \| null |  |  | ID of an existing clothing item for try-on generation |
| clothing_item_ids | body | no | array<integer> |  |  | IDs of existing clothing items for multi-item generation |
| avatar_id | body | no | integer \| null |  |  | ID of a saved avatar. If not provided, a virtual model will be used |
| model_slug | body | yes | string |  | See model catalog below | Required model slug for unified generation jobs. Choose the model explicitly because pricing and capabilities vary by model. Current slugs, pricing, and capabilities are listed below. |
| use_case | body | no | string |  | generate, edit, upscale, video | Generation use case. Omit or use generate for standard try-on images |
| prompt | body | yes | string |  |  | Natural language description of the desired image, emphasizing the model appearance and scene |
| num_images | body | yes | integer |  |  | Number of images to generate (1-5) |
| camera | body | no | string | photo |  | Camera angle for the shot. 'photo' (recommended) keeps auto framing, while explicit cameras request front/back/side views. Supported values come from GET /cameras. |
| aspect_ratio | body | no | string |  | auto, 21:9, 16:9, 3:2, 4:3, 5:4, 1:1, 4:5, 3:4, 2:3, 9:16 | Optional aspect ratio when supported by the selected model. Current unified generation catalog values: auto, 21:9, 16:9, 3:2, 4:3, 5:4, 1:1, 4:5, 3:4, 2:3, 9:16. |
| resolution | body | no | string | 2K | 720p, 1K, 768X1024, 1024X1280, 2K, 4K | Optional output resolution when supported by the selected model. Current unified generation catalog values: 720p, 1K, 768X1024, 1024X1280, 2K, 4K. |
| img_ref_urls | body | no | array<string> |  |  | Reference image URLs when supported by the selected model. The current unified generation catalog allows up to 9 reference images; selected models may allow fewer. |
| generation_result_parent_id | body | no | integer |  |  | Existing generation result to use as the source for edit, upscale, or video jobs. Use image_url instead for an external source image |
| image_url | body | no | string |  |  | External source image URL for edit, upscale, or video jobs. Do not send together with generation_result_parent_id |
| last_frame_url | body | no | string |  |  | Optional final keyframe URL for video models that support first-frame/last-frame generation. |
| duration | body | no | integer |  | 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 | Video duration in seconds. Current model catalog values: 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15. |
| generate_audio | body | no | boolean | false |  | Generate audio when supported by the selected video model. Some models price audio separately. |
| upscale_factor | body | no | number | 2 | 2, 4 | Upscale factor when supported by the selected model. Current model catalog values: 2, 4. |
| target_resolution | body | no | string | 2160p | 720p, 1080p, 1440p, 2160p | Target output resolution for upscale models that support it. Current model catalog values: 720p, 1080p, 1440p, 2160p. |
| feature_setting | body | no | object |  |  | Advanced feature-specific options |
| webhook_url | body | no | string |  |  | Optional request-level callback URL. Omit this to use the saved webhook endpoint configured on the API Keys page. |
| webhook_secret | body | no | string |  |  | Optional request-level signing secret for webhook_url. Saved webhook endpoints use the generated secret shown on the API Keys page. |
| webhook_events | body | no | array<string> |  |  | Optional request-level webhook events. Supported values are generation.completed and generation.failed. |
| enhance_user_prompt | body | no | boolean | true |  | Let AI enhance your prompt for better results. Set to false only with well-crafted prompts |


#### Image and edit models
| Model | Slug | Credits | Capabilities |
| --- | --- | --- | --- |
| Gemini Flash 2 | `nano-banana-2` | 3-7 credits | resolutions: 1K, 2K, 4K; 10 aspect ratios; 3 refs |
| Gemini Pro | `nano-banana-pro` | 5-10 credits | resolutions: 1K, 2K, 4K; 10 aspect ratios; 3 refs |
| GPT Image 2 (high) | `gpt-image-2-high` | 12 credits | resolutions: 1K, 2K; 10 aspect ratios; 3 refs |
| GPT Image 2 (medium) | `gpt-image-2-medium` | 6 credits | resolutions: 1K, 2K; 10 aspect ratios; 3 refs |
| GPT Image 2 (low) | `gpt-image-2-low` | 2 credits | resolutions: 1K, 2K; 10 aspect ratios; 3 refs |
| SeedDream 4.5 | `seedream-v4-5` | 2 credits | resolutions: 1K, 2K, 4K; 10 aspect ratios; 3 refs |
| Qwen Intimate | `qwen-rapid-aio-v23` | 1-2 credits | resolutions: 768X1024, 1024X1280; 1 refs |
| Gemini Flash | `gemini-flash` | 1 credit | 10 aspect ratios; 3 refs |


#### Upscale models
| Model | Slug | Credits | Capabilities |
| --- | --- | --- | --- |
| SeedVR2 Upscale | `seedvr2` | 1 credit | upscale: 2x, 4x; target: 4K |
| Aura SR Upscale | `aura-sr` | 1 credit | upscale: 4x; target: 4K |


#### Video models
| Model | Slug | Credits | Capabilities |
| --- | --- | --- | --- |
| Seedance 2 | `seedance-2` | 49-183 credits | resolutions: 720p; 7 aspect ratios; 9 refs; duration: 4-15 sec; audio |
| Kling 3 Pro | `kling-3-pro` | 14-101 credits | 3 refs; duration: 3-15 sec; audio; last frame |
| Kling 2.5 Turbo Pro | `kling-2-5-turbo-pro` | 14-26 credits | duration: 5-10 sec; last frame |
| Seedance 1.5 Pro | `seedance-1-5-pro` | 6-20 credits | duration: 5-10 sec; audio; last frame |


#### Example Request

```json
{
  "clothing_item_id": 1,
  "model_slug": "nano-banana-2",
  "use_case": "generate",
  "prompt": "female model wearing the clothing, professional studio photography",
  "num_images": 2,
  "camera": "full_body_front",
  "aspect_ratio": "9:16",
  "resolution": "2K",
  "img_ref_urls": [],
  "enhance_user_prompt": true,
  "avatar_id": null
}
```


#### Example Response

```json
{
  "generation_id": 789,
  "clothing_item_ids": [
    123
  ],
  "num_images": 2,
  "payload": "{\"prompt\":\"female model wearing the clothing, professional studio photography\",\"camera\":\"full_body_front\",\"model_slug\":\"nano-banana-2\",\"use_case\":\"generate\",\"resolution\":\"2K\",\"aspect_ratio\":\"9:16\"}",
  "status": "Created",
  "feature_name": "model:nano-banana-2",
  "created_at": "2024-01-15T15:30:00Z",
  "updated_at": "2024-01-15T15:30:00Z",
  "avatar_id": null
}
```


### POST /generation
**Create Upscale Generation**
Create an upscale job through the unified internal generation route. Send use_case=upscale with a source generation result or image URL. Webhook callbacks for terminal events include outputs in data.results.

#### Request Body Parameters
| Name | Location | Required | Type | Default | Allowed values | Description |
| --- | --- | --- | --- | --- | --- | --- |
| generation_result_parent_id | body | no | integer |  |  | ID of a previously generated result. Required if image_url is not provided |
| image_url | body | no | string |  |  | URL of any image. Required if generation_result_parent_id is not provided |
| model_slug | body | yes | string |  | See model catalog below | Required model slug for upscale jobs. Choose the model explicitly because pricing and capabilities vary by model. Current slugs, pricing, and capabilities are listed below. |
| use_case | body | yes | string |  | upscale | Set to upscale for image enhancement jobs |
| num_images | body | yes | integer | 1 |  | Number of outputs to create |
| upscale_factor | body | no | number | 2 | 2, 4 | Upscale factor when supported by the selected model. Current model catalog values: 2, 4. |
| target_resolution | body | no | string | 2160p | 720p, 1080p, 1440p, 2160p | Target output resolution for upscale models that support it. Current model catalog values: 720p, 1080p, 1440p, 2160p. |
| feature_setting | body | no | object |  |  | Advanced model-specific options |
| webhook_url | body | no | string |  |  | Optional request-level callback URL. Omit this to use the saved webhook endpoint configured on the API Keys page. |
| webhook_secret | body | no | string |  |  | Optional request-level signing secret for webhook_url. Saved webhook endpoints use the generated secret shown on the API Keys page. |
| webhook_events | body | no | array<string> |  |  | Optional request-level webhook events. Supported values are generation.completed and generation.failed. |


#### Upscale models
| Model | Slug | Credits | Capabilities |
| --- | --- | --- | --- |
| SeedVR2 Upscale | `seedvr2` | 1 credit | upscale: 2x, 4x; target: 4K |
| Aura SR Upscale | `aura-sr` | 1 credit | upscale: 4x; target: 4K |


#### Example Request

```json
{
  "generation_result_parent_id": 1234,
  "model_slug": "seedvr2",
  "use_case": "upscale",
  "num_images": 1,
  "upscale_factor": 2,
  "target_resolution": "2160p"
}
```


#### Example Response

```json
{
  "generation_id": 901,
  "created_at": "2024-01-15T17:00:00Z",
  "updated_at": "2024-01-15T17:00:00Z"
}
```


### POST /generation
**Create Video Generation**
Transform a static image into a video through the unified internal generation route. Send use_case=video with a source generation result or image URL. Webhook callbacks for terminal events include outputs in data.results.

#### Request Body Parameters
| Name | Location | Required | Type | Default | Allowed values | Description |
| --- | --- | --- | --- | --- | --- | --- |
| generation_result_parent_id | body | no | integer \| null |  |  | ID of a previously generated result. Required if image_url is not provided. Set to null when using image_url |
| image_url | body | no | string |  |  | URL of any image. Required if generation_result_parent_id is not provided |
| img_ref_urls | body | no | array<string> |  |  | Reference image URLs for video models that support them. The current video catalog allows up to 9 reference images; selected models may allow fewer. |
| last_frame_url | body | no | string |  |  | Optional final keyframe URL for video models that support first-frame/last-frame generation. |
| model_slug | body | yes | string |  | See model catalog below | Required model slug for video jobs. Choose the model explicitly because pricing and capabilities vary by model. Current slugs, pricing, and capabilities are listed below. |
| use_case | body | yes | string |  | video | Set to video for image-to-video jobs |
| num_images | body | yes | integer | 1 |  | Number of video outputs to create |
| prompt | body | no | string |  |  | Natural language description to guide the video motion and style |
| duration | body | yes | integer |  | 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 | Video duration in seconds. Current model catalog values: 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15. |
| generate_audio | body | no | boolean | false |  | Generate audio when supported by the selected video model. Some models price audio separately. |
| resolution | body | yes | string |  | 720p | Optional video resolution when supported by the selected model. Current video catalog values: 720p. |
| aspect_ratio | body | no | string |  | auto, 21:9, 16:9, 4:3, 1:1, 3:4, 9:16 | Optional video aspect ratio when supported by the selected model and no first frame is supplied. Current video catalog values: auto, 21:9, 16:9, 4:3, 1:1, 3:4, 9:16. |
| webhook_url | body | no | string |  |  | Optional request-level callback URL. Omit this to use the saved webhook endpoint configured on the API Keys page. |
| webhook_secret | body | no | string |  |  | Optional request-level signing secret for webhook_url. Saved webhook endpoints use the generated secret shown on the API Keys page. |
| webhook_events | body | no | array<string> |  |  | Optional request-level webhook events. Supported values are generation.completed and generation.failed. |


#### Video models
| Model | Slug | Credits | Capabilities |
| --- | --- | --- | --- |
| Seedance 2 | `seedance-2` | 49-183 credits | resolutions: 720p; 7 aspect ratios; 9 refs; duration: 4-15 sec; audio |
| Kling 3 Pro | `kling-3-pro` | 14-101 credits | 3 refs; duration: 3-15 sec; audio; last frame |
| Kling 2.5 Turbo Pro | `kling-2-5-turbo-pro` | 14-26 credits | duration: 5-10 sec; last frame |
| Seedance 1.5 Pro | `seedance-1-5-pro` | 6-20 credits | duration: 5-10 sec; audio; last frame |


#### Example Request

```json
{
  "generation_result_parent_id": null,
  "image_url": "https://app-uwear-staging.s3.us-east-1.amazonaws.com/generation-results/8613/edit/test_bf45a773-e846-45f4-ab85-19827f32a0fa.png",
  "model_slug": "kling-3-pro",
  "use_case": "video",
  "num_images": 1,
  "prompt": "fashion model posing for a fashion photoshoot",
  "duration": 5,
  "img_ref_urls": [],
  "generate_audio": false
}
```


#### Example Response

```json
{
  "generation_id": 912,
  "payload": "{\"image_url\":\"https://app-uwear-staging.s3.us-east-1.amazonaws.com/generation-results/8613/edit/test_bf45a773-e846-45f4-ab85-19827f32a0fa.png\",\"model_slug\":\"kling-3-pro\",\"prompt\":\"fashion model posing for a fashion photoshoot\",\"duration\":5,\"use_case\":\"video\",\"generate_audio\":false}",
  "created_at": "2024-01-15T18:00:00Z",
  "updated_at": "2024-01-15T18:00:00Z"
}
```


### POST /generation
**Create Edit Generation**
Apply AI-powered edits through the unified internal generation route. Send use_case=edit with a source generation result or image URL. Webhook callbacks for terminal events include outputs in data.results.

#### Request Body Parameters
| Name | Location | Required | Type | Default | Allowed values | Description |
| --- | --- | --- | --- | --- | --- | --- |
| generation_result_parent_id | body | no | integer |  |  | ID of a previously generated result. Required if image_url is not provided |
| image_url | body | no | string |  |  | URL of any image. Required if generation_result_parent_id is not provided |
| model_slug | body | yes | string |  | See model catalog below | Required model slug for edit jobs. Choose the model explicitly because pricing and capabilities vary by model. Current slugs, pricing, and capabilities are listed below. |
| use_case | body | yes | string |  | edit | Set to edit for image editing jobs |
| num_images | body | yes | integer | 1 |  | Number of edited images to create |
| prompt | body | yes | string |  |  | Natural language instructions for the desired edits (e.g., "remove the background", "change lighting to sunset", "add a hat") |
| aspect_ratio | body | no | string |  | 21:9, 16:9, 3:2, 4:3, 5:4, 1:1, 4:5, 3:4, 2:3, 9:16 | Optional aspect ratio when supported by the selected model. Current edit catalog values: 21:9, 16:9, 3:2, 4:3, 5:4, 1:1, 4:5, 3:4, 2:3, 9:16. |
| resolution | body | no | string | 2K | 1K, 768X1024, 1024X1280, 2K, 4K | Optional output resolution when supported by the selected model. Current edit catalog values: 1K, 768X1024, 1024X1280, 2K, 4K. |
| img_ref_urls | body | no | array<string> |  |  | Reference image URLs when supported by the selected model. The current edit catalog allows up to 3 reference images; selected models may allow fewer. |
| webhook_url | body | no | string |  |  | Optional request-level callback URL. Omit this to use the saved webhook endpoint configured on the API Keys page. |
| webhook_secret | body | no | string |  |  | Optional request-level signing secret for webhook_url. Saved webhook endpoints use the generated secret shown on the API Keys page. |
| webhook_events | body | no | array<string> |  |  | Optional request-level webhook events. Supported values are generation.completed and generation.failed. |


#### Image and edit models
| Model | Slug | Credits | Capabilities |
| --- | --- | --- | --- |
| Gemini Flash 2 | `nano-banana-2` | 3-7 credits | resolutions: 1K, 2K, 4K; 10 aspect ratios; 3 refs |
| Gemini Pro | `nano-banana-pro` | 5-10 credits | resolutions: 1K, 2K, 4K; 10 aspect ratios; 3 refs |
| GPT Image 2 (high) | `gpt-image-2-high` | 12 credits | resolutions: 1K, 2K; 10 aspect ratios; 3 refs |
| GPT Image 2 (medium) | `gpt-image-2-medium` | 6 credits | resolutions: 1K, 2K; 10 aspect ratios; 3 refs |
| GPT Image 2 (low) | `gpt-image-2-low` | 2 credits | resolutions: 1K, 2K; 10 aspect ratios; 3 refs |
| SeedDream 4.5 | `seedream-v4-5` | 2 credits | resolutions: 1K, 2K, 4K; 10 aspect ratios; 3 refs |
| Qwen Intimate | `qwen-rapid-aio-v23` | 1-2 credits | resolutions: 768X1024, 1024X1280; 1 refs |
| Gemini Flash | `gemini-flash` | 1 credit | 10 aspect ratios; 3 refs |


#### Example Request

```json
{
  "generation_result_parent_id": 1234,
  "model_slug": "nano-banana-2",
  "use_case": "edit",
  "num_images": 1,
  "prompt": "Change the background to a beach sunset with warm lighting",
  "aspect_ratio": "9:16",
  "resolution": "2K",
  "img_ref_urls": []
}
```


#### Example Response

```json
{
  "generation_id": 923,
  "created_at": "2024-01-15T19:00:00Z",
  "updated_at": "2024-01-15T19:00:00Z"
}
```


## Generation Results
Access the output images from your generation requests. Each result includes the generated image URLs and metadata. Note: Generated images are only available for 4 hours after creation.

### GET /generation-results
**Get All Generation Results**
Retrieve a paginated list of generation results with optional filtering by generation ID or clothing item ID.

#### Parameters
| Name | Location | Required | Type | Default | Allowed values | Description |
| --- | --- | --- | --- | --- | --- | --- |
| generation_ids | query | no | array<integer> |  |  | Filter results by generation IDs. Repeat the query parameter for multiple IDs |
| clothing_item_ids | query | no | array<integer> |  |  | Filter results by clothing item IDs. Repeat the query parameter for multiple IDs |
| page | query | no | integer |  |  | Page number for pagination |
| items_per_page | query | no | integer |  |  | Number of items per page |


#### Example Request

```json
{
  "generation_ids": [
    789
  ],
  "page": "1",
  "items_per_page": "20"
}
```


#### Example Response

```json
{
  "current_page": 1,
  "max_page": 2,
  "total_count": 30,
  "data": [
    {
      "generation_result_id": 1234,
      "generation_id": 789,
      "url": "https://app-uwear-prod.s3.us-east-1.amazonaws.com/generation-results/8613/image/test_zapier_403483.png",
      "kind": "Image",
      "created_at": "2024-01-15T15:32:00Z",
      "updated_at": "2024-01-15T15:32:00Z",
      "clothing_item_id": 123,
      "available": true,
      "origin": "api"
    },
    {
      "generation_result_id": 1235,
      "generation_id": 789,
      "url": "https://app-uwear-prod.s3.us-east-1.amazonaws.com/generation-results/8613/image/test_zapier_284172.png",
      "kind": "Image",
      "created_at": "2024-01-15T15:32:00Z",
      "updated_at": "2024-01-15T15:32:00Z",
      "clothing_item_id": 123,
      "available": true,
      "origin": "api"
    }
  ]
}
```


### GET /generation-result/{generation_result_id}
**Get Generation Result Details**
Get detailed information about a specific generation result by its ID, including image URLs and metadata.

#### Parameters
| Name | Location | Required | Type | Default | Allowed values | Description |
| --- | --- | --- | --- | --- | --- | --- |
| generation_result_id | path | yes | integer |  |  | The ID of the generation result to retrieve |


#### Example Request

```json
{
  "generation_result_id": "1234"
}
```


#### Example Response

```json
{
  "generation_result_id": 1234,
  "generation_id": 789,
  "url": "https://app-uwear-prod.s3.us-east-1.amazonaws.com/generation-results/8613/image/test_zapier_284170.png",
  "kind": "Image",
  "created_at": "2024-01-15T15:32:00Z",
  "updated_at": "2024-01-15T15:32:00Z",
  "clothing_item_id": 123,
  "available": true,
  "origin": "api"
}
```


## Avatars
Create and manage persistent avatars for consistent model representation across generations. Avatars allow you to maintain the same virtual model appearance across multiple clothing generations.

### GET /avatars
**Get All Avatars**
Retrieve a paginated list of all your avatars.

#### Parameters
| Name | Location | Required | Type | Default | Allowed values | Description |
| --- | --- | --- | --- | --- | --- | --- |
| page | query | no | integer |  |  | Page number for pagination |
| items_per_page | query | no | integer |  |  | Number of items per page |


#### Example Request

```json
{
  "page": "1",
  "items_per_page": "10"
}
```


#### Example Response

```json
{
  "current_page": 1,
  "max_page": 2,
  "total_count": 15,
  "data": [
    {
      "avatar_id": 101,
      "avatar_name": "Summer Model",
      "avatar_url": "https://storage.uwear.ai/avatars/101.jpg",
      "thumbnail_url": "https://storage.uwear.ai/avatars/101_thumb.jpg",
      "avatar_description": {
        "body": "athletic female",
        "age": 25
      },
      "count_generation_results": 4,
      "generation_result_id": null,
      "created_at": "2024-01-10T10:00:00Z",
      "updated_at": "2024-01-10T10:00:00Z"
    }
  ]
}
```


### GET /avatar/{avatar_id}
**Get Avatar Details**
Get detailed information about a specific avatar by its ID, including its name and associated image.

#### Parameters
| Name | Location | Required | Type | Default | Allowed values | Description |
| --- | --- | --- | --- | --- | --- | --- |
| avatar_id | path | yes | integer |  |  | The ID of the avatar to retrieve |


#### Example Request

```json
{
  "avatar_id": "101"
}
```


#### Example Response

```json
{
  "avatar_id": 101,
  "avatar_name": "Summer Model",
  "avatar_url": "https://storage.uwear.ai/avatars/101.jpg",
  "thumbnail_url": "https://storage.uwear.ai/avatars/101_thumb.jpg",
  "avatar_description": {
    "body": "athletic female",
    "age": 25
  },
  "count_generation_results": 4,
  "generation_result_id": null,
  "created_at": "2024-01-10T10:00:00Z",
  "updated_at": "2024-01-10T10:00:00Z"
}
```


### POST /avatar
**Save Avatar**
Save a generated image or external image as a persistent avatar for reuse across multiple generations. AI enhancement can automatically extract physical characteristics from the image if needed.

#### Request Body Parameters
| Name | Location | Required | Type | Default | Allowed values | Description |
| --- | --- | --- | --- | --- | --- | --- |
| avatar_name | body | yes | string |  |  | User-friendly name for your avatar |
| avatar_url | body | yes | string |  |  | URL of the avatar image to save |
| avatar_description | body | no | object { body, age } |  |  | Physical characteristics of the avatar |
| avatar_enhancement | body | no | boolean | false |  | Enable AI vision to automatically extract body type and age from the image. Note: AI-generated descriptions will overwrite manual input |


#### Example Request

```json
{
  "avatar_name": "Professional Model",
  "avatar_url": "https://app-uwear-prod.s3.us-east-1.amazonaws.com/generation-results/8613/image/avatar-source.png",
  "avatar_description": {
    "body": "athletic female",
    "age": 28
  },
  "avatar_enhancement": false
}
```


#### Example Response

```json
{
  "avatar_id": 102,
  "avatar_name": "Professional Model",
  "avatar_url": "https://app-uwear-prod.s3.us-east-1.amazonaws.com/avatars/102/avatar_image.jpg",
  "avatar_description": {
    "body": "athletic female",
    "age": 28
  },
  "count_generation_results": 0,
  "generation_result_id": null,
  "created_at": "2024-01-15T20:00:00Z",
  "updated_at": "2024-01-15T20:00:00Z"
}
```


### PUT /avatar/{avatar_id}
**Update Avatar**
Update an existing avatar's name and description. Note: To change the avatar image, create a new avatar with the updated image.

#### Parameters
| Name | Location | Required | Type | Default | Allowed values | Description |
| --- | --- | --- | --- | --- | --- | --- |
| avatar_id | path | yes | integer |  |  | The ID of the avatar to update |


#### Request Body Parameters
| Name | Location | Required | Type | Default | Allowed values | Description |
| --- | --- | --- | --- | --- | --- | --- |
| avatar_name | body | no | string |  |  | Updated name for the avatar |
| avatar_description | body | no | object { body, age } |  |  | Updated physical characteristics of the avatar |


#### Example Request

```json
{
  "avatar_id": "102",
  "avatar_name": "Fashion Model Pro",
  "avatar_description": {
    "body": "athletic female",
    "age": 28
  }
}
```


#### Example Response

```json
{
  "avatar_id": 102,
  "avatar_name": "Fashion Model Pro",
  "avatar_url": "https://storage.uwear.ai/avatars/102.jpg",
  "avatar_description": {
    "body": "athletic female",
    "age": 28
  },
  "count_generation_results": 5,
  "generation_result_id": null,
  "created_at": "2024-01-15T20:00:00Z",
  "updated_at": "2024-01-15T20:30:00Z"
}
```


### DELETE /avatar/{avatar_id}
**Delete Avatar**
Delete an avatar by its ID. This operation is irreversible.

#### Parameters
| Name | Location | Required | Type | Default | Allowed values | Description |
| --- | --- | --- | --- | --- | --- | --- |
| avatar_id | path | yes | integer |  |  | The ID of the avatar to delete |


#### Example Request

```json
{
  "avatar_id": "102"
}
```


#### Example Response

```json
{
  "message": "Avatar deleted successfully"
}
```

