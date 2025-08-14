import fs from 'fs';
import path from 'path';
import fetch from 'node-fetch';

const JSON_PATH = 'src/data/cms2.json';
const IMAGE_DIR = 'public/images/noticias/';

async function processImages() {
  // 1. Read and parse the JSON file
  let jsonData;
  try {
    const rawData = fs.readFileSync(JSON_PATH);
    jsonData = JSON.parse(rawData);
    console.log('Successfully read JSON file.');
  } catch (error) {
    console.error(`Error reading or parsing JSON file at ${JSON_PATH}:`, error);
    return;
  }

  const noticias = jsonData.noticias;
  if (!noticias || !Array.isArray(noticias)) {
    console.error('The key "noticias" is not a valid array in the JSON file.');
    return;
  }

  // 2. Create directory if it doesn't exist
  if (!fs.existsSync(IMAGE_DIR)) {
    fs.mkdirSync(IMAGE_DIR, { recursive: true });
    console.log(`Created directory: ${IMAGE_DIR}`);
  }

  // 3. Loop through news items, download images, and update paths
  for (const noticia of noticias) {
    const imageUrl = noticia.imagen;
    if (!imageUrl || typeof imageUrl !== 'string') {
      console.warn('Skipping item with invalid image URL:', noticia);
      continue;
    }

    // Handle the malformed URL
    const correctedUrl = imageUrl.replace('https://images//', 'https://www.cmsconsultores.cl/images/');
    const filename = path.basename(new URL(correctedUrl).pathname);
    const localPath = path.join(IMAGE_DIR, filename);
    const publicPath = `/images/noticias/${filename}`;

    console.log(`Processing: ${correctedUrl}`);
    console.log(` -> Saving to: ${localPath}`);

    try {
      const response = await fetch(correctedUrl);
      if (!response.ok) {
        throw new Error(`Failed to fetch ${correctedUrl}: ${response.statusText}`);
      }
      const buffer = await response.buffer();
      fs.writeFileSync(localPath, buffer);

      // Update the JSON object with the new local path
      noticia.imagen = publicPath;
      console.log(`   -> Success.`);

    } catch (error) {
      console.error(`   -> Failed to download or save image for ${correctedUrl}. Error:`, error.message);
      // If download fails, we keep the original URL
    }
  }

  // 4. Write the updated JSON back to the file
  try {
    fs.writeFileSync(JSON_PATH, JSON.stringify(jsonData, null, 4));
    console.log('Successfully updated JSON file with new image paths.');
  } catch (error) {
    console.error('Error writing updated JSON file:', error);
  }
}

processImages();
