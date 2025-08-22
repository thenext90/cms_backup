import { list, put, del } from '@vercel/blob';

export const POST = async ({ request }) => {
  try {
    const newContact = await request.json();
    const blobName = 'contactos.json';
    let contacts = [];

    // List blobs with a prefix to find our specific file
    const { blobs } = await list({ prefix: blobName, limit: 1 });
    const contactBlob = blobs.find(b => b.pathname === blobName);

    if (contactBlob) {
      // If the blob exists, fetch its content
      const response = await fetch(contactBlob.url);
      if (response.ok) {
        const text = await response.text();
        if (text) {
          try {
            const parsed = JSON.parse(text);
            if(Array.isArray(parsed)) {
                contacts = parsed;
            }
          } catch (parseError) {
            // The blob is not valid JSON, maybe it was corrupted.
            // We can decide to overwrite it.
            console.error('Failed to parse existing contacts.json, will overwrite.', parseError);
          }
        }
      }
    }

    // Add a timestamp to the new contact
    newContact.timestamp = new Date().toISOString();
    contacts.push(newContact);

    // Upload the updated list, overwriting the old one
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
    const errorMessage = error instanceof Error ? error.message : String(error);
    return new Response(JSON.stringify({ message: 'Error saving contact', error: errorMessage }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
};
