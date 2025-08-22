import { put, head, del } from '@vercel/blob';

export const POST = async ({ request }) => {
  try {
    const newContact = await request.json();

    let contacts = [];
    const blobName = 'contactos.json';

    let blobInfo = null;
    try {
      blobInfo = await head(blobName);
    } catch (error) {
      if (error.status !== 404) {
        // Re-throw if it's not a 'not found' error
        throw error;
      }
    }

    if (blobInfo) {
      // If blob exists, get its content
      const response = await fetch(blobInfo.url);
      if (response.ok) {
        const text = await response.text();
        // It might be an empty file, so we check
        if (text) {
          contacts = JSON.parse(text);
        }
      }
    }

    // Add new contact
    contacts.push(newContact);

    // Upload the updated list to Vercel Blob
    await put(blobName, JSON.stringify(contacts, null, 2), {
      access: 'public',
      contentType: 'application/json',
    });

    return new Response(JSON.stringify({ message: 'Contact saved successfully' }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (error) {
    console.error('Error in API route:', error);
    return new Response(JSON.stringify({ message: 'Error saving contact', error: error.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
};
